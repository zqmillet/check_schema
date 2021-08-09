import pytest
import queue
import collections

from check_schema import load_schema
from check_schema.exceptions import TypeMismatchException

class Dict(dict): pass
class List(list): pass
class Int(int): pass

@pytest.fixture(name='schema_string')
def _schema_string():
    return """
    type: dict
    properties:
        x:
            type: int
            required: false
        y:
            type: [int, float]
            required: false
        z:
            type: [str, None]
            required: false
        w:
            type: [collections.UserDict, queue.Queue]
            required: false
        a:
            type: type
            required: false
        l:
            type: list
            required: false
            items:
                type: null
    """

@pytest.mark.parametrize(
    'data', [
        dict(),
        Dict(),
        dict(x=1, y=2.0),
        dict(z=None, y=2),
        dict(z='None', y=2),
        Dict(a=int, w=queue.Queue()),
        Dict(a=list, w=collections.UserDict()),
        Dict(l=list()),
        Dict(l=List()),
        Dict(l=List([None, None])),
        Dict(l=[None, None]),
    ]
)
def test_check_type_fuzzy(schema_string, data):
    schema = load_schema(schema_string)
    schema.check(data)
    
def test_check_type_strictly(schema_string):
    schema = load_schema(schema_string, mode='strictly')
    class Dict(dict): pass

    with pytest.raises(TypeMismatchException):
        schema.check(Dict())
