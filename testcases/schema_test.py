import pytest

from check_schema import load_schema
from check_schema.exceptions import TypeMismatchException

def test_check_type_fuzzy():
    string = """
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

    schema = load_schema(string)
    schema.check(dict())
    schema.check(dict(a=1, b=2))
    
    with pytest.raises(TypeMismatchException):
        schema.check({'x': 'x'})

def test_check_type_():
    string = """
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

    schema = load_schema(string, mode='strictly')
    class Dict(dict): pass
    with pytest.raises(TypeMismatchException):
        schema.check(Dict())


