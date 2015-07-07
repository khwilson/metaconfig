metaconfig
==========

Some people at [work](https://www.knewton.com) were asking me about metaclasses in Python and
what they are good for. There's a great quote about from Tim Peters about them that goes

> Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder
> whether you need them, you don't....

I actually don't think that's entirely true, but it's pretty accurate. In particular,
metaclasses can make completing very specific tasks much more elegant even if there
were other ways to avoid them, e.g., with class decorators or descriptors. For instance,
you could accomplish a registry by using a class decorator, which since a single class
might get registered multiple times for different purposes but it can only have one
metaclass might actually be preferable.

To give an example for my work friends about when metaclasses might be a more elegant
solution, I've written an example of a type of config loader. The idea is pretty
banal: You've got a bunch of configs from all your service clients and depending upon
what you're doing (e.g., some local place for testing or some (set of) standard
locations in deployment), your config might be in a different standard place.

These classes aren't perfect, and there's probably some nicer style things I could do,
but I think they illustrate how metaclasses work and how they may improve the elegance
of something that definitely has multiple solutions.

Installation
------------

This isn't on PyPI right now. Just `pip install` directly from this gitub repo. The
installation requires `PyYAML`.

Usage
-----

Config classes should use `MetaConfig` as the metaclass. MetaConfigs have various
`Field`s, of which several are provided by default.

```python
import metaconfig

class SimpleConfig(object):
    __metaclass__ = metaconfig.Config

    int_field = metaconfig.IntField('A basic int field', 0)
    str_field = metaconfig.StrField('A basic str field')
    unicode_field = metaconfig.UnicodeField('A basic unicode field', u'')
    bytes_field = metaconfig.BytesField('A basic bytes field')
    float_field = metaconfig.FloatField('A basic float field')
    bool_field = metaconfig.BoolField()
    tuple_field = metaconfig.TupleField('A simple tuple field')
```

In this example, I've made a simple config that has many different fields of various
types (this is Python 2, obviously, so pardon the many string classes). The first argument
to each `\*Field` is a docstring. The second argument is a default value. These are both
optional.

The `Field` types have very little logic, essentially just casting the values assigned
to them and raising a `ValueError` if the cast fails.

Once you have declared your config, you can build a yaml that looks somthing like

```python
import textwrap

yaml_config = textwrap.dedent("""
    int_field: 10
    str_field: hello world
    bytes_field: some bytes
    float_field: 1.3802
    bool_field: true
    tuple_field:
        - 4
        - 5
""")
```

Then to use the config, you can simple `loads` the config from a string.

```python
>>> config = SimpleConfig()
>>> config.loads(yaml_config)
>>> print yaml_config.int_field
10
```

The library also handles nested configs either through the unstructured `DictField`,
or if you want to add structure, you can use the `ConfigField`.

