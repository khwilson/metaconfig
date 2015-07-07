"""
A configuration scheme that allows you to specify the expected form of a config
ahead of time, do some validation, and also have docstrings on the various properties
of the config.

@author Kevin Wilson - khwilson@gmail.com
"""
import copy

import yaml

from .metafields import Field


def _gen_getter(hidden_key):
    """
    A closure that generates a getter for properties for the given key
    """
    def getter(_self):
        return getattr(_self, hidden_key)
    return getter


def _gen_setter(hidden_key, value):
    """
    A closure that generates a setter for properties for the given key in a Field
    """
    def setter(_self, val):
        setattr(_self, hidden_key, value.validate(val))
    return setter


class MetaConfig(type):
    """
    A configuration object that will, upon initialization, set many standard functions and
    initialization procedures for configs, including setting up descriptors for Fields
    based on class fields declared in the config.
    """

    def __init__(self, name, bases, dct):
        # All elements must be Fields and declared ahead of time
        self.__all_keys = []
        for key, value in dct.iteritems():
            if not isinstance(type(value), Field):
                continue

            self.__all_keys.append(key)
            hidden_key = '__' + key
            setattr(self, hidden_key, value.validate(value.default))
            setattr(self, key, property(_gen_getter(hidden_key), _gen_setter(hidden_key, value),
                                        None, value.doc))

        def load(_self, from_file=None):
            """ Load a config from a file """
            if from_file is None:
                from_file = paths.get_config_path(getattr(_self, resource_type),
                                                  getattr(_self, resource_name))

            with open(from_file, 'r') as f:
                _self.loads(f.read())

        def loads(_self, from_str):
            """ Load a config from a string """
            yml = yaml.load(from_str)
            _self.from_dict(yml)

        def from_dict(_self, yml):
            """ Load a config from a YAML-like dict """
            yml = copy.copy(yml)
            for key in _self.__all_keys:
                if key not in yml:
                    continue
                setattr(_self, key, yml[key])
                del yml[key]

            if yml:
                raise TypeError("There were extra keys provided in the "
                                "configuration than were specified in the MetaConfig")

        def init(self, dct=None):
            if dct:
                self.from_dict(dct)

        setattr(self, 'load', load)
        setattr(self, 'loads', loads)
        setattr(self, 'from_dict', from_dict)
        setattr(self, '__init__', init)


class ResourceConfig(MetaConfig):
    """
    A type of MetaConfig that declares where it expects its on disk configurations to
    be relative to a standard directory.
    """
    def __init__(self, names, bases, dct):
        # Set the resource_type and resource_name
        for field in ['resource_type', 'resource_name']:
            if field not in dct:
                raise AttributeError("A ResourceConfig must have a {}".format(field))
            setattr(self, field, dct[field])
        MetaConfig.__init__(self, names, bases, dct)
