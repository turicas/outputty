outputty
========

`outputty` is a simple Python library that helps you importing, filtering and
exporting data. It is composed by a main `Table` class and a lot of plugins
that helps importing and exporting data to/from `Table` (in future we'll have
filtering plugins). You can write your own plugin easily (see
`outputty/plugin_*.py` for examples).

Some examples of plugins are: CSV, text, HTML and histogram.

Installation
------------

- [Download the package](https://github.com/turicas/outputty/tarball/master)
- Extract it
- Copy the directory `outputty` (inside the extracted folder) to some folter
  you can do `import outputty` (it can be your system's `site-packages` or even
  your project's path).

Sorry for that - it'll be available in PyPI soon.


Examples
--------

You can run all the examples below - see `examples` folder. You can also see
the tests we have at `tests/test_*.py`.

{{EXAMPLES}}

Type Of Data
------------

`outputty` will try to convert every element inside a row to `unicode`. In
strings it'll use `string.decode(input_encoding)`, where `input_encoding` is
specified in `Table.__init__`. For other types (integer, float etc.) it'll use
`unicode(element)`.


Character Encodings
-------------------

Received strings are decoded using __UTF-8__ and output is encoded also using
__UTF-8__ by default. You can change this behaviour with the parameters
`input_encoding` and `output_encoding` to `Table`, for example:

    my_table = Table(headers=['Column 1', 'Column 2'], input_encoding='iso-8859-1',
                     output_encoding='utf16')

You can also get the table string decoded, in unicode:

    table_in_unicode = unicode(my_table)

> See [Standard Encodings in
> Python](http://docs.python.org/library/codecs.html#standard-encodings) to get a
> complete list of the supported encodings.

> `headers` must be a list of strings.


### Encoding and Decoding

- __Decoding__: if you need `table.headers` and table rows in unicode,
  just call `table.decode()` and it'll decode all data using
  `table.input_encoding` (you can pass an alternative codec as parameter).
- __Encoding__: if you need `table.headers` and table and rows encoded to some
  codec, just call `table.decode()` and it'll encode all data using
  `table.output_encoding` (you can pass an alternative codec as parameter).


Notes About Data Normalization
------------------------------

We have two kinds of normalization in `Table`:

- `.normalize_types()`: used by default when importing from CSV, this method
  convert table rows to the types it identify. All data that in first moment
  are strings will be converted to `unicode`, `int`, `float`, `datetime.date`
  or `datetime.datetime` when identified.

> If you want all your data as `unicode` when importing from CSV you can pass
> `convert_types=False` to `Table` so it won't use `normalize_types` after
> importing data (it'll just decode your strings using `input_encoding`).

- `unicode` normalization: all operations in `Table` (import from some format,
  output table in some format, normalization and ordering) will convert data
  internally to `unicode` using `input_encoding` as codec (passed in
  `Table.__init__`). When `convert_types=False`, all row's values will be
  `unicode`, otherwise only types identified as string will be converted to
  `unicode`.


### `to_list_of_dicts` and `to_dict`

If you want to access all table rows as dicts, just convert it using the
method `to_list_of_dicts`. Using the same table from Example 1, if we execute:

    rows = my_table.to_list_of_dicts()
    print rows[1]['First Name']

...it'll print:

    Flávio

You can also convert your table to a `dict`, with header names as keys and
columns as values and filter which columns will go to the dictionary:

    table_dict = my_table.to_dict()
    print table_dict

    table_dict_filtered = my_table.to_dict(only=['First Name', 'Last Name'])
    print table_dict_filtered

...will print:

    {'Last Name': (u'Justen', u'Amieiro'), 'First Name': (u'\xc1lvaro', u'Fl\xe1vio'), 'Main Language': (u'Python', u'Python')}
    {'Last Name': (u'Justen', u'Amieiro'), 'First Name': (u'\xc1lvaro', u'Fl\xe1vio')}

And if you want to create a `dict` with some column value as key and other
column value as value you can specify `key` and `value` parameters, as in:

    other_table = Table(headers=['date', 'measure'])
    other_table.append(('2011-12-01', 21))
    other_table.append(('2011-12-02', 42))
    other_table.append(('2011-12-03', 3.14))
    other_table.append(('2011-12-04', 2.71))
    values_as_dict = other_table.to_dict(key='date', value='measure')
    print values_as_dict

...that produces:

    {'2011-12-04': 2.71, '2011-12-03': 3.14, '2011-12-02': 42, '2011-12-01': 21}


New Features
------------

Yes, there are a lot of features to add (it's just the begining). If you
want to contribute, please see our
[WISHLIST.markdown](https://github.com/turicas/outputty/blob/master/WISHLIST.markdown)
file.

You can also use the [Github Issue Tracking
System](https://github.com/turicas/outputty/issues) to report bugs.


Contributing
------------

If you want to contribute to this project, please:

- Use [Test-driven
  development](http://en.wikipedia.org/wiki/Test-driven_development)
- Create your new feature in branch `feature/name-of-the-new-feature`
  (`git checkout -b feature/new-feature`)
- Run __all tests__ (`make test`) _before_ pushing
  - To run just one test file, execute: `nosetests --with-coverage --cover-package outputty  tests/test_your-test-file.py`
  - Try to have a test-coverage of 100%
- To run tests, execute `make test`. I use some `nose` plugins -- to install
  it, execute: `pip install nose coverage ipdbplugin yanc`
- Create/update documentation (README/docstrings/man page)
  - __Do NOT edit `README.markdown`.__ Edit `README-template.markdown` and run
  `make create-readme` to create the new `README.markdown` based on
  `README-template.markdown` and files on `examples/` (the "Examples" section
  is created automatically).


### New Plugins

If you want to create a new plugin to import/export from/to some new
resource, please see files `outputty/plugin_*.py` - they are simple: you just
need to create `read` and/or `write` functions that will received the `Table`
object and, optionally, the parameters you want. Save your file in
`outputty/plugin_name.py`, where `name` is the name of your plugin.

To call your plugin, just execute: `my_table.write('name', optional_parameters)`
or `my_table.read('name', optional_parameters)` (where `name` is the name of
your plugin), then `outputty` will call `outputty.plugin_name.read` or
`outputty.plugin_name.write`.

### Contributors

My sincerely thanks to:

- [Fundação Getúlio Vargas](http://www.fgv.br/) for letting me invest my time
  on it.
- [Douglas Andrade](https://github.com/douglas) for showing me
  `textwrap.dedent` and writting more legible tests.
- [Flávio Coelho](https://github.com/fccoelho) for creating `histogram` and
  giving a lot of suggestions.
- [Renne Rocha](https://github.com/rennerocha) for creating `order_by`.
- [Tatiana Al-Chueyr](https://github.com/tatiana) for helping me design the
  simple yet powerful plugin API.
- [Flávio Amieiro](https://github.com/flavioamieiro) for a lot of suggestions
  and interpretations about design.


Related Software
----------------

- [fabulous](http://lobstertech.com/fabulous.html)
- [termcolor](http://pypi.python.org/pypi/termcolor)
- [tablib](https://github.com/kennethreitz/tablib)
- [clint](https://github.com/kennethreitz/clint)
- [csvstudio](http://code.google.com/p/csvstudio/)
- [PyTables](http://www.pytables.org/)
- [pyspread](http://manns.github.com/pyspread/)
