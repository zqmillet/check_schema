from check_schema import load_schema

def test_load_schema():
    string = '''
    type: dict
    properties:
        x:
            type: int
            assertion: "lambda x: x > 0"
        y:
            type: int
            assertion: "lambda x: x >= 0"
        person:
            type: list
            items:
                type: dict
                properties:
                    name:
                        type: str
                    age:
                        type: [int, None]
                        assertion: "lambda x: x is None"
        array:
            type: list
            items:
                - type: int
                - type: float
                  assertion: "lambda x: x ** 2 < 100"
                - type: [str, null]
    assertion: "lambda x: len(x) > 0"
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

    assert callable(schema['assertion'])
    assert callable(schema['properties']['x']['assertion'])
    assert callable(schema['properties']['y']['assertion'])
    assert callable(schema['properties']['array']['items'][1]['assertion'])
    assert callable(schema['properties']['person']['items']['properties']['age']['assertion'])
