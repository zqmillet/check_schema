from check_schema import load_schema
from check_schema import Schema

def test_load_schema():
    string = '''
    type: dict
    properties:
        x:
            type: int
        y:
            type: int
        person:
            type: list
            items:
                type: dict
                properties:
                    name:
                        type: str
                    age:
                        type: [int, None]
        array:
            type: list
            items:
                - type: int
                - type: float
                - type: [str, null]
        
    '''
    schema = load_schema(string)
    assert schema['type'] == (dict,)
    assert schema['properties']['x']['type'] == (int,)
    assert schema['properties']['y']['type'] == (int,)
    assert schema['properties']['person']['items']['type'] == (dict,)
    assert schema['properties']['person']['items']['properties']['name']['type'] == (str,)
    assert schema['properties']['person']['items']['properties']['age']['type'] == (int, type(None))

    assert schema['properties']['array']['type'] == (list,)
    assert schema['properties']['array']['items'][0]['type'] == (int,)
    assert schema['properties']['array']['items'][1]['type'] == (float,)
    assert schema['properties']['array']['items'][2]['type'] == (str, type(None))
