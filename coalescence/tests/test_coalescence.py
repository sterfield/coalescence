import pytest
import coalescence.main
import coalescence.exception

class TestMix():

    def test_add_source(self, sourced_mix, source_map_1):
        assert 's1' in sourced_mix._sources
        assert 's2' in sourced_mix._sources
        assert sourced_mix._sources['s1'].priority == 1
        assert sourced_mix._sources['s1'].name == 's1'
        assert sourced_mix._sources['s1'].object == source_map_1

    def test_sources_property(self, sourced_mix):
        assert sourced_mix.sources == ['s1', 's2']

    def test_serialize(self, sourced_mix, mix_schema):
        result = sourced_mix.serialize(mix_schema, sourced_mix)
        assert isinstance(result['fourth'], coalescence.main.Leaf)
        assert isinstance(result['second'], coalescence.main.Branch)
    
    def test_serialize_incorrect_variable(self, sourced_mix):
        schema = {
            '1st': {
                'type': 'str',
                'values': {
                    's1': {
                        'path': 'first element',
                        'priority': 1
                    },
                    's2': {
                        'path': '1',
                        'priority': 2
                    }
                }
            }
        }
        with pytest.raises(coalescence.exception.SerializationException) as e:
            sourced_mix.serialize(schema, sourced_mix)

    def test_load_schema_no_source(self, mix, mix_schema):
        with pytest.raises(coalescence.exception.NoSuchSourceException) as e:
            mix.load_schema(mix_schema)

    def test_load_schema(self, sourced_mix, mix_schema):
        sourced_mix.load_schema(mix_schema)
        assert 'first' in sourced_mix._branches
        assert 'second' in sourced_mix._branches
        assert 'third' in sourced_mix._branches
        assert 'fourth' in sourced_mix._branches
        assert isinstance(sourced_mix._branches['first'], coalescence.main.Leaf)

    def test_getattribute(self, loaded_mix):
        assert loaded_mix.first == loaded_mix._branches['first']


class TestBranch():

    def test_getattribute(self, branch):
        assert branch._branches['sub'] == branch.sub

class TestLeaf():

    def test_value_created_with_own_prioriy(self, leaf):
        assert leaf._values['s1'].priority == 1

    def test_value_created_with_source_prioriy(self, leaf):
        assert leaf._values['s2'].priority == 2

class TestHelper():

    def test_is_leaf(self, mix_schema):
        assert coalescence.main.is_leaf(mix_schema['first'])

    def test_is_not_leaf(self, mix_schema):
        assert not coalescence.main.is_leaf(mix_schema['second'])

class TestDocumentation():
    """Test the use case in the documentation"""

    def test_documentation_use_case(self, mix):
        import os
        os.environ = {'DEBUG': '1'}
        cli = {'--debug': True}
        config = {'debug': 'false'}
        mix.add_source('envvars', os.environ, 10)
        mix.add_source('conffile', config, 1)
        mix.add_source('cli', cli, 5)
        schema = {
            'debug': {
                'type': 'bool',
                'values': {
                    'envvars': {
                        'path': 'DEBUG'
                    },
                    'conffile': {
                        'path': 'debug'
                    },
                    'cli': {
                        'path': '--debug'
                    }
                }
            }
        }
        mix.load_schema(schema)
        assert mix.debug.value == True
        os.environ['DEBUG'] = '0'
        assert mix.debug.value == False


        