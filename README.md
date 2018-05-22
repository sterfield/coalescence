# Coalescence

## Introduction
Coalescence is a small library that merge the content of several dictionaries with different keys in one central object.

Let's take an example : you are building a project, and to configure this project, you rely on multiple sources :
- command line options
- configuration file
- environment variables

Most likely, you'll have the same options in several, potentially all your configuration sources : `--debug` in command line, `debug = false` in the configuration file, `DEBUG=1` in envvars. 

Now, you have three objects in your code, that represents the same thing, but are vastly different :
- keys are different
- value's type are different (in the above example `bool` for cli, `str` for conffile and `int` for envvars)
- there's no notion of priority among those. Command line options says `debug` is activated, but the configuration file says otherwise. Which one is right ?

So you'll put in your code many `if…else` to handle the merge of those configuration : 
```python
if os.environ['DEBUG'] == 1 or cli['--debug'] or config['debug'] == 'false':
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)
```


Coalescence allow you to create a central object that will aggregate the content of multiple sources, with priorities between source and value casted to the chosen type. 

Create a `Mix` object, that will aggregate all your configuration:
```python
import coalescence

my_config = coalescence.Mix()
```
Declare your object sources. The number will indicate the priority (higher = more priority)
```python
my_config.add_source('envvars', os.environ, 10)
my_config.add_source('conffile', config, 1)
my_config.add_source('cli', cli, 5)
```
Define the schema of your Mix object. It's a regular python object with a specific format. The `values` object indicates the source that will be checked, and the `path` the name of the key in the source's object.
```python
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
my_config.load_schema(schema)
```
That's it !
Now you have one object tha holds all your configuration, in one place in your code.
```python
my_config.debug.value
# Envvars have higher priority. return True
```
Change the source and the value will update accordingly
```python
os.environ['DEBUG'] = '0'
my_config.debug.value
# envvars have higher priority. return False
```


