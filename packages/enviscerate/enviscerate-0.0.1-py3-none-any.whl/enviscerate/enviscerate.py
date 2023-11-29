from warnings import warn

try:
    from jsonofabitch import loads
except:
    warn("jsonofabitch module not found, defaulting to builtin json")
    from json import loads
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    warn("dotenv not found, not loading values from $PWD/.env")


import traceback
from os import getenv

YES = ["t", "true", "1", "yes", "y"]


def env(val=None):
    (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
    def_name = text[: text.find("=")].strip()
    if type(val) is bool:
        return getenv(def_name, str(val)).lower() in YES
    elif type(val) is dict:
        _envval = getenv(def_name, False)
        if _envval:
            return loads(_envval)
        else:
            return val
    elif val is None:
        return(getenv(def_name,None))
    else:
        return type(val)(getenv(def_name, val))
