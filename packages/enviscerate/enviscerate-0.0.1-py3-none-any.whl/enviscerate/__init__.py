"""One line access to environment variables, handling typecasts automatically. Simply declare a variable with the same name, assigning it to the output of the function ``env(default_value)`` where ``default_value`` is of the type you want the env variable casted as. It is easier to say with an example:

from enviscerate import env
HOME = env('/this/dir')

Will set the value of HOME with the following precedence 

1. env var ``$HOME``
2. .env file supplied value
3. value ``'/this/dir'`` you supplied to env() function above


features
--------

- if type is dict, it will be parsed as JSLOB using jsonofabitch module(if available). parsed as JSON using builtin json.loads() otherwise
- if bool it will be set to ``True`` if ``str(val).lower() in ["t", "true", "1", "yes", "y"]`` for ``env(val)`` and ``False`` otherwise
- If ``None``, the case of ``env()``, you will get ``None`` if the variable is not declared and a string otherwise
- otherwise it will be casted as whatever you supply. presumably an ``int`` ``float`` or ``str`` but with no presumptions or restrictions thereof
- It will use dotenv if available but does not require it, but will spit warnings to avoid frustrating mysterious why-are-my-settings-not-registering hickups

"""

from .enviscerate import env
from .enviscerate import YES

__all__ = ["env","YES"]

__version__: str = "0.0.1"
