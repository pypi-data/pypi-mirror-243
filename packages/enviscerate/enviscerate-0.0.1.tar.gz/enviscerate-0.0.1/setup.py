import os
import re

from setuptools import setup

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except Exception:
    long_description = ""
(__version__,) = re.findall(
    '__version__: str = "(.*)"', open("enviscerate/__init__.py").read()
)


setup(
    name="enviscerate",
    description="Access env variables by one line declaration with automatic typecasting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=[
        "enviscerate",
    ],
    install_requires=[],
    requires=[],
    keywords=["dotenv", "env", "vars", "environment", "shell", "bash"],
    license="MIT",
)
