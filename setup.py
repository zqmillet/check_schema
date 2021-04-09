from setuptools import setup

from check_schema import __author__
from check_schema import __email__
from check_schema import __module_name__
from check_schema import __description__
from check_schema import __url__
from check_schema import __version__

setup(
    name=__module_name__,
    version='.'.join(map(str, __version__)),
    description=__description__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    packages=['check_schema']
)
