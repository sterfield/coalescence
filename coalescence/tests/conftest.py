import pytest
import coalescence.main

@pytest.fixture
def mix_schema():
    return {
        'first': {
            'type': 'str',
            'values': {
                's1': {
                    'path': 'first element',
                    'priority': 1
                },
                's2': {
                    'path': '1',
                }
            }
        },
        'second': {
            'sub': {
                'type': 'int',
                'values': {
                    's1': {
                        'path': 'second',
                        'priority': 1
                    },
                    's2': {
                        'path': '2["2 bis"]',
                        'priority': 3
                    }
                }
            }
        },
        'third': {
            'type': 'float',
            'values': {
                's1': {
                    'path': 'third.val',
                    'priority': 3
                },
                's2': {
                    'path': '3',
                    'priority': 1
                }
            }
        },
        'fourth': {
            'type': 'bool',
            'values': {
                's1': {
                    'path': 'fourth',
                    'priority': 1
                },
                's2': {
                    'path': '4',
                    'priority': 1
                }
            }
        },
    }

@pytest.fixture
def source_map_1():
    return {
        'first element': 'this is a string',
        'second': 42,
        'third': {'val': 18.5},
        'fourth': True
    }

@pytest.fixture
def source_map_2():
    return {
        '1': 'another string',
        '2': {'2 bis': 7},
        '3': 3.14,
        '4': False
    }

@pytest.fixture
def mix():
    return coalescence.main.Mix()

@pytest.fixture
def sourced_mix(mix, source_map_1, source_map_2):
    mix.add_source('s1', source_map_1, 1)
    mix.add_source('s2', source_map_2, 2)
    return mix

@pytest.fixture
def loaded_mix(sourced_mix, mix_schema):
    sourced_mix.load_schema(mix_schema)
    return sourced_mix

@pytest.fixture
def branch(loaded_mix):
    return loaded_mix.second

@pytest.fixture
def leaf(loaded_mix):
    return loaded_mix.first