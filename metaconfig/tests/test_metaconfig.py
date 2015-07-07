import textwrap
import unittest

import metaconfig


class SimpleConfig(object):
    __metaclass__ = metaconfig.MetaConfig

    int_field = metaconfig.IntField('A basic int field', 0)
    str_field = metaconfig.StrField('A basic str field')
    unicode_field = metaconfig.UnicodeField('A basic unicode field', u'')
    bytes_field = metaconfig.BytesField('A basic bytes field')
    float_field = metaconfig.FloatField('A basic float field')
    bool_field = metaconfig.BoolField()
    dict_field = metaconfig.DictField('A crazy dict field')
    tuple_field = metaconfig.TupleField('A simple tuple field')


SimpleConfigField = metaconfig.gen_config_field('SimpleConfigField', 'SimpleConfig', SimpleConfig)


class NestedConfig(object):
    __metaclass__ = metaconfig.ResourceConfig

    nested_field = SimpleConfigField('A field for SimpleConfigs')

    resource_type = 'test'
    resource_name = 'alot'


class TestMetaConfig(unittest.TestCase):

    def setUp(self):
        self.basic_config = textwrap.dedent("""
            int_field: 10
            str_field: hello world
            dict_field:
                a: 1
                b: 2
                c: 3
            bytes_field: some bytes
            float_field: 1.3802
            bool_field: true
            tuple_field:
                - 4
                - 5
            """)

    def _validate_simple_config(self, test_config):
        self.assertEqual(10, test_config.int_field)
        self.assertEqual('hello world', test_config.str_field)
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, test_config.dict_field)
        self.assertEqual('some bytes', test_config.bytes_field)
        self.assertEqual(u'', test_config.unicode_field)
        self.assertEqual(1.3802, test_config.float_field)
        self.assertEqual(True, test_config.bool_field)
        self.assertEqual((4, 5), test_config.tuple_field)

    def test_simple_config(self):
        test_config = SimpleConfig()
        test_config.loads(self.basic_config)
        self._validate_simple_config(test_config)

    def test_nested_config(self):
        str_nested_config = "nested_field:\n" + self.basic_config.replace('\n', '\n  ')
        test_config = NestedConfig()
        test_config.loads(str_nested_config)
        self._validate_simple_config(test_config.nested_field)
