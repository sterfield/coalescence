import weakref
import logging
import builtins

import coalescence.exception


logger = logging.getLogger(__name__)


class Source():

    def __init__(self, name, obj, priority):
        self.object = obj
        self.priority = priority
        self.name = name


class Value():

    def __init__(self, source=None, path=None, priority=None, element=None):
        self.element = element
        self._source = source
        self._path = path
        self.priority = priority

    @property
    def value(self):
        try:
            obj = self.element.sources[self._source].object
            return obj[self._path]
        except KeyError:
            raise

class Leaf():

    def __init__(self, type=int, name=None, path=None, values={}, default=False, default_value=None, parent=None):
        self.parent = parent
        self.name = name
        self._path = path
        self.type = type 
        self.default = default
        self.default_value = default_value
        self._values={}
        
        self.serialize(values)

    @staticmethod
    def get_sources(current_node):
        if hasattr(current_node, '_sources'):
            return current_node._sources
        else:
            return Leaf.get_sources(current_node.parent)

    @property
    def sources(self):
        return Leaf.get_sources(self.parent)

    def serialize(self, sources):
        for source, value in sources.items():
            if source not in self.sources:
                logger.critical(f"source name '{source}' doesn't exist in the current list of sources")
                raise coalescence.exception.NoSuchSourceException
            logger.info(f"Adding a source '{source}' for the value '{self.name}'")
            if 'priority' not in value:
                value['priority'] = self.sources[source].priority
            self._values[source] = Value(**value, element=self, source=source)

    @staticmethod
    def cast(value_type, value):
        if isinstance(value_type, str):
            logger.info(f"Type has been entered as a string. Searching for its Python type")
            if not value_type in builtins.__dict__:
                logger.critical(f"type {value_type} is not a builtin type !")
                raise coalescence.exception.CoercetionException
            value_type = getattr(builtins, value_type)
        if value_type == bool and value == '0':
            logger.debug(f"Special case : casting bool('0') == True, which is not what we want. So forcing False")
            return False
        try:
            return value_type(value)
        except ValueError:
            logger.critical(f"Cannot cast '{value}' in type '{value_type}'")
            raise coalescence.exception.CoercetionException

    @property
    def value(self):
        priority = -1
        result = None
        for value in self._values.values():
            if value.priority > priority:
                try:
                    result = value.value
                except KeyError:
                    continue
                priority = value.priority
        if result == None:
            if not self.default:
                raise coalescence.exception.NoValueException
            else:
                Leaf.cast(self.type ,self.default_value)
        else:
            return Leaf.cast(self.type, result)

            

def is_leaf(branch):
    if 'values' in branch:
        return True
    else:
        return False

class Branch():

    def __init__(self, parent, name=None):
        self._branches = {}
        self.parent = parent
        self.name = name

    def __getattribute__(self, name):
        try:
            return super().__getattribute__('_branches')[name]
        except KeyError:
            raise AttributeError
    
    def __getattr__(self, name):
        return super().__getattribute__(name)

class Mix():

    def __init__(self):
        self._sources = {}
        self._branches = {}

    @staticmethod
    def serialize(schema, parent):
        result = {}
        for key, value in schema.items():
            if not key.isidentifier():
                logger.critical(f"The node name '{key}is not a valid Python variable !")
                logger.critical(f"A variable must start with an underscore or a letter")
                raise coalescence.exception.SerializationException
            if is_leaf(value):
                result[key] = Leaf(**value, parent=parent, name=key)
            else:
                branch = Branch(parent=parent, name=key)
                weak_branch = weakref.proxy(branch)
                branch._branches = Mix.serialize(value, weak_branch)
                result[key] = branch
        return result

    def load_schema(self, schema):
        if not self._sources:
            raise coalescence.exception.NoSuchSourceException
        weak_self = weakref.proxy(self)
        self._branches = self.serialize(schema, weak_self)

    @property
    def sources(self):
        return [source for source in self._sources]
    
    def add_source(self, name, obj, priority, primary_source=False):
        logger.info(f"Adding source '{name}'")
        self._sources[name] = Source(name, obj, priority)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__('_branches')[name]
        except KeyError:
            raise AttributeError

    def __getattr__(self, name):
        return super().__getattribute__(name)  

