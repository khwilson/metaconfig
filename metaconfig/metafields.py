"""
A metaclass which describes a Field to be used by MetaConfig descriptors.

@author Kevin Wilson - khwilson@gmail.com
"""

class Field(type):
    def __new__(self, name, bases, dct):
        if 'validate' not in dct:
            raise AttributeError("A Field must have a method `validate`")

        if '__init__' not in dct:
            def default_init(self, doc=None, default=None):
                self.doc = doc
                self.default = default

            dct['__init__'] = default_init

        return type.__new__(self, name, bases, dct)


def _gen_basic_field(name_of_field, name_of_type, the_type):
    """
    Given a type the_type, generate a basic field which casts the passed argument to the_type
    if it is not None, else return None.

    :param str name_of_field: The name of the basic field
    :param str name_of_type: The name of the type
    :param type the_type: The type to cast to
    :rtype: Field
    :return: The generated Field type
    """
    def validate(self, x):
        return None if x is None else the_type(x)

    doc = "A field which can be {name_of_type} or None".format(name_of_type=name_of_type)

    return Field(name_of_field, (), {'validate': validate, '__doc__': doc})


IntField = _gen_basic_field('IntField', 'int', int)
StrField = _gen_basic_field('StrField', 'str', str)
UnicodeField = _gen_basic_field('UnicodeField', 'unicode', unicode)
BytesField = _gen_basic_field('BytesField', 'bytes', bytes)
FloatField = _gen_basic_field('FloatField', 'float', float)
BoolField = _gen_basic_field('BoolField', 'bool', bool)
DictField = _gen_basic_field('DictField', 'dict', dict)
TupleField = _gen_basic_field('TupleField', 'tuple', tuple)


def gen_config_field(name_of_field, name_of_type, the_type):
    """
    Generate a Field type that will validate a `Config`.

    :param str name_of_field: The name of the field
    :param str name_of_type: The name of the Config type
    :param type the_type: The actual Config type
    :rtype: Field
    :return: The generated Field type
    """
    return _gen_basic_field(name_of_field, name_of_type, the_type)
