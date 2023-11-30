import os
import re
from typing import List
from collections.abc import Mapping, MutableMapping

_envre = re.compile(r"""^(?:export\s*)?([_a-zA-Z][\w_]*)\s*=\s*(.*)$""")
_varexp = re.compile(r"""\{\{(.*?)\}\}""")
_varname = re.compile(r"""^\s*([\w_]+)\s*$""")
_include_re = re.compile(r"""^#include\s+(.*)\s*$""")


def _cast_bool(value):
    try:
        if int(value) == 1:
            return True
        return False
    except:
        pass

    if value.lower() in ["true", "yes", "on"]:
        return True
    elif value.lower() in ["false", "no", "off"]:
        return False

    raise ValueError("Invalid boolean value: {}".format(value))


class Environment(MutableMapping):
    def __init__(self, data: Mapping, prefix=None):
        self._data = dict(data)
        self.prefix = prefix
        self.prefixf = lambda x: x if not prefix else f"{prefix}_{x}"

    def expand_variables(self, value):
        if type(value) is not str:
            return value

        for var in _varexp.findall(value):
            match = _varname.match(var)
            if not match:
                raise Exception(f"[{var}]: invalid variable name")

            varname = match.group(1)
            if varname not in self:
                raise Exception(f"[{varname}]: unbounded variable")

            value = value.replace(f"{{{{{var}}}}}", self[varname])

        return value

    def union(self, other: Mapping):
        return Environment({**self, **other}, prefix=self.prefix)

    def get(self, key: str, default=None, nullable=False, mapper=None):
        if not mapper:

            def mapper(x):
                return x

        if mapper is bool:
            mapper = _cast_bool

        value = super().get(self.prefixf(key)) or self._data.get(key)

        if value is not None:
            return mapper(value)

        if default is None and not nullable:
            raise KeyError(key)
            # raise Exception(f"{key} not found. Declare it as environment variable or provide a default value.")

        return mapper(default)

    def __call__(self, key: str, default=None, nullable=False, cast=lambda x: x):
        return self.get(key, default, nullable, cast)

    def __setitem__(self, key, value):
        self._data[key] = self.expand_variables(value)

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self) -> str:
        return "{}({{{}}})".format(
            type(self).__name__,
            ", ".join(
                ("{!r}: {!r}".format(key, value) for key, value in self._data.items())
            ),
        )


class DotEnv(Environment):
    def _load_env(self, env_file: str):
        env_file = os.path.abspath(env_file)

        if env_file in self.envs:
            return

        self.envs.add(env_file)

        if not os.path.isfile(env_file):
            return

        with open(env_file, "r") as f:
            for line in f.readlines():
                match = _include_re.match(line)
                if match is not None:
                    file = match.group(1).strip()
                    self._load_env(file)

                match = _envre.match(line)
                if match is not None:
                    key = match.group(1)
                    value = match.group(2).strip('"').strip("'")

                    self[key] = value

        return vars

    def __init__(self, *env_files, **kwargs):
        super(DotEnv, self).__init__({}, **kwargs)
        self.envs = set()

        for file in env_files:
            self._load_env(file)


def enrich_environ(*env_files, **kwargs):
    if len(env_files) == 0:
        env_files = [".env"]

    for key, value in DotEnv(*env_files, **kwargs).items():
        if key not in os.environ:
            os.environ[key] = value


def path_mapper(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    path = os.path.realpath(path, strict=True)
    path = os.path.normpath(path)

    return path


import lark
from lark import Transformer
from datetime import datetime
from lark.visitors import Discard

parser = lark.Lark(
    r"""
start: includes* exps*

exps: exp  | exp exps
exp: pair NEWLINE | COMMENT NEWLINE
pair: "export"? CNAME "=" value? ";"? COMMENT?

value: SIGNED_INT 
    | SIGNED_FLOAT 
    | STRING 
    | UNQUOTED_STRING
    | BOOL
    | "[" atoms "]"  
    | "{" atoms "}"  -> atomic_set

atoms.1: ints | strings | floats 
ints: SIGNED_INT | SIGNED_INT "," ints            
strings: STRING | STRING "," strings                
floats: SIGNED_FLOAT | SIGNED_FLOAT "," floats   
includes: include | include includes  
include: "@include" /"[^"\r\n]*?"/ NEWLINE

BOOL.1: /true|false/i
UNQUOTED_STRING: /[^'"\r\n=]+/
STRING: /'[^'\r\n]*?'|"[^"\r\n]*?"/ 
COMMENT: /#[^\n\r]*/

%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.NEWLINE
%import common.WS
%import common.CNAME
%ignore WS
%ignore NEWLINE

"""
)


class _visitor(Transformer):
    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)
        self.include_paths = []

        def get_val(token):
            return token.value

        def get_typed_val(token):
            if token.type == "SIGNED_INT":
                return int(token.value)
            if token.type == "SIGNED_FLOAT":
                return float(token.value)
            if token.type == "STRING":
                return token.value[1:-1]
            if token.type == "UNQUOTED_STRING":
                return token.value
            if token.type == "BOOL":
                return token.value.lower() == "true"

            raise Exception(f"{token.type}: unknown token type")

        self.SIGNED_INT = get_typed_val
        self.SIGNED_FLOAT = get_typed_val
        self.STRING = get_typed_val
        self.UNQUOTED_STRING = get_typed_val
        self.BOOL = get_typed_val
        # self.include = get_typed_val

        self.CNAME = get_val

    def NEWLINE(self, _):
        return None

    def COMMENT(self, _):
        return Discard

    def value(self, children):
        return children[0]

    def atomic_set(self, children):
        return set(children[0])

    def atoms(self, children):
        result = []
        cur = children[0]
        while len(cur.children) > 0:
            result.append(cur.children[0])
            if len(cur.children) == 1:
                break
            cur = cur.children[1]
        return result


    def pair(self, children):
        if len(children) == 1:
            return Discard
        return {"key": children[0], "value": children[1]}

    # def include(self, children):
    #     return children[0].value[1:-1]

    def includes(self, children):
        self.include_paths.append(children[0].children[0].value[1:-1])
        return Discard

    def start(self, children):
        return {child["key"]: child["value"] for child in children}


f = """
@include "file1"
@include "file2"
# comment 1
export a = true
TOKEN = "key1";
nn = "a;b" # comment 2
l =[1,3,4 , 4]
s = {1,2,3, 3}
b=1.3
c=
ee = abcde
_c = "a"
n = 3
"""

# tree = parser.parse(f)
# exp = _visitor(visit_tokens=True).transform(tree)

# print(exp)
