import yaml
import enum
import importlib

from check_schema.exceptions import TypeMismatchException
from check_schema.exceptions import InitializeLambdaExpressionException
from check_schema.exceptions import AssertionException
from check_schema.exceptions import CannotFindPropertyException
from check_schema.exceptions import EnumerationException
from check_schema.exceptions import InvalidPropertyException
from check_schema.exceptions import DependenciesException
from check_schema.exceptions import RegexPatternException
from check_schema.exceptions import NonstringTypeHasPatternException
from check_schema.exceptions import ExceedMaximumException
from check_schema.exceptions import ExceedMinimumException
from check_schema.exceptions import LengthRangeException
from check_schema.exceptions import MultipleOfException


class Mode(enum.Enum):
    fuzzy = 'fuzzy'
    strictly = 'strictly'

class Schema(dict):
    type_map = {
        'int': int,
        'float': float,
        'str': str,
        'dict': dict,
        'set': set,
        'list': list,
        'tuple': tuple,
        'any': object,
        'None': type(None),
        'type': type,
        None: type(None)
    }

    def __init__(self, configuration, mode=Mode.fuzzy):
        super().__init__(configuration)
        self._handle_type()
        self._handle_assertion()
        self._handle_properties()
        self._handle_items()
        if mode == Mode.fuzzy:
            self._is_type = isinstance
        else:
            self._is_type = lambda instance, types: type(instance) in types

    def _handle_properties(self):
        properties = self.get('properties', dict())
        for name, _configuration in properties.items():
            properties[name] = Schema(_configuration)

    def _handle_items(self):
        if isinstance(self.get('items'), dict):
            self['items'] = Schema(self['items'])
        elif isinstance(self.get('items'), list):
            self['items'] = [Schema(item) for item in self['items']]

    def _handle_type(self):
        _type = self['type']
        if not isinstance(_type, list):
            types = [_type]
        else:
            types = _type

        self['type'] = tuple([self._load_type(_type) for _type in types])

    def _handle_assertion(self):
        expression = self.get('assertion')
        if not expression:
            return

        try:
            lambda_expression = eval(expression) # pylint: disable = eval-used
        except Exception:
            raise InitializeLambdaExpressionException(expression) from None
        
        self['assertion'] = lambda_expression

    def _load_type(self, _type):
        _type = str(_type)
        if _type in self.type_map:
            return self.type_map[_type]

        *packages, clazz = _type.rsplit('.')
        module = importlib.import_module('.'.join(packages))
        return getattr(module, clazz)

    def _check_type(self, data, name):
        if not self._is_type(data, self['type']):
            raise TypeMismatchException(data, self['type'], name)

    def _check_properties(self, data, name):
        if 'properties' not in self: 
            return

        for property_name, property_schema in self['properties'].items():
            required = property_schema.get('required', True)

            if property_name not in data and required:
                raise CannotFindPropertyException(
                    data=data,
                    property_name=property_name,
                    name=name
                )

            if property_name not in data:
                continue

            dependencies = property_schema.get('dependencies', list())
            for dependency in dependencies:
                if dependency in data:
                    continue

                raise DependenciesException(
                    data=data,
                    name=name,
                    property_name=property_name,
                    nonexistent_dependencies=sorted(set(dependencies) - data.keys())
                )

            property_schema.check(
                data=data[property_name],
                name='{name}[{property_name}]'.format(name=name, property_name=repr(property_name))
            )

        additional_properities = sorted(set(data) - self['properties'].keys())
        if not self.get('additional_properities', True) and additional_properities:
            raise InvalidPropertyException(
                data=data,
                property_names=additional_properities,
                name=name
            )

    def check(self, data, name='data'):
        self._check_type(data, name)
        self._check_properties(data, name)

def load_schema(string, mode=Mode.fuzzy):
    return Schema(yaml.safe_load(string), mode)
