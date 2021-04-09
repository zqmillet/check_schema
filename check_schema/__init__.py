"""
description: this module provides the function check_schema.
"""

from .check_schema import check_schema

from .exceptions import SchemaException
from .exceptions import TypeMismatchException
from .exceptions import AssertionException
from .exceptions import InitializeLambdaExpressionException
from .exceptions import CannotFindPropertyException
from .exceptions import EnumerationException
from .exceptions import InvalidPropertyException
from .exceptions import DependenciesException
from .exceptions import RegexPatternException
from .exceptions import NonstringTypeHasPatternException
from .exceptions import ExceedMaximumException
from .exceptions import ExceedMinimumException
from .exceptions import LengthRangeException
from .exceptions import MultipleOfException

__author__ = 'qiqi'
__email__ = 'zqmillet@qq.com'
__module_name__ = 'check_schema'
__description__ = 'check object with schema'
__url__ = 'https://github.com/zqmillet/check_schema'
__version__ = (0, 0, 1)
