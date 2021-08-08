import yaml
import importlib

from check_schema.exceptions import InitializeLambdaExpressionException

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
    }

    def __init__(self, configuration):
        super().__init__(configuration)
        self._handle_type()
        self._handle_assertion()
        self._handle_properties()
        self._handle_items()

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
        if isinstance(_type, str):
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

def load_schema(string):
    return Schema(yaml.safe_load(string))
