outputty
========

`outputty` is just a Python library that helps you importing, filtering and
exporting data. It is composed by a main `Table` class and a lot of plugins
that helps importing and exporting data to/from `Table`. You can write your own
plugin easily (see `outputty/plugin_*.py` for examples).

Some examples of plugins are: CSV, text, HTML and histogram.

Installation
------------

Just copy the file `outputty.py` in some path you can do `import outputty`
(sorry for that - it'll be available in PyPI soon).


Examples
--------

You can run all the examples below - see `examples` folder. You can also see
the tests we have at `tests/test_*.py`.

### Example 1: Basics of `Table`

A `Table` is a list of rows. These rows can be represented with `dict`-like,
`list`-like and `tuple`-like objects. Let's create one and prints it to
stdout.

If you have this code, like in `examples/1_table.py`: 
        
    from outputty import Table
    my_table = Table(headers=['First Name', 'Last Name', 'Main Language'])
    my_table.append({'First Name': 'Álvaro', 'Last Name': 'Justen',
                          'Main Language': 'Python'})
    my_table.append(('Flávio', 'Amieiro', 'Python'))
    print my_table

After executing it, you'll get this output:

    +------------+-----------+---------------+
    | First Name | Last Name | Main Language |
    +------------+-----------+---------------+
    |     Álvaro |    Justen |        Python |
    |     Flávio |   Amieiro |        Python |
    +------------+-----------+---------------+
    

### Example 2: Exporting to a CSV File

Using plugins we can import and export `Table` data to CSV (really, to and
from a lot of formats). Let's export Python `list` and `dict` to a CSV file.

If you have this code, like in `examples/2_table_to_csv.py`: 
        
    from outputty import Table
    
    my_table = Table(headers=['First name', 'Last name'])
    my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
    my_table.append(('Flávio', 'Amieiro'))
    my_table.write('csv', 'my-data.csv')

The file `my-data.csv` will be created with this content:

    "First name","Last name"
    "Álvaro","Justen"
    "Flávio","Amieiro"


### Example 3: Exporting to a Text File

We can also import data from a CSV file and export it to a text file (using
plugins, again).

If you have the file `nice-software.csv` with these contents:

    id,name,website
    1,Python,http://www.python.org/
    2,OpenSSH,http://www.openssh.com/
    3,fabric,http://fabfile.org/


and do you have the code below, like in `examples/3_table_to_text_file.py`: 
        
    from outputty import Table
    
    my_table = Table()
    my_table.read('csv', 'nice-software.csv')
    my_table.write('text', 'nice-software.txt')

The file `nice-software.txt` will be created with this content:

    +----+---------+-------------------------+
    | id |   name  |         website         |
    +----+---------+-------------------------+
    |  1 |  Python |  http://www.python.org/ |
    |  2 | OpenSSH | http://www.openssh.com/ |
    |  3 |  fabric |     http://fabfile.org/ |
    +----+---------+-------------------------+

### Example 4: Ordering `Table` Data

You can order your table's data with the method `Table.order_by`.
You need to specify a column in which the ordering will be based on and
optionally specify if the ordering will be ascending (default) or descending.

If you have this code, like in `examples/4_order_by.py`: 
        
    from outputty import Table
    
    my_table = Table(headers=['First name', 'Last name'])
    my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
    my_table.append({'First name': 'Renne'})
    my_table.append(('Flávio', 'Amieiro'))
    my_table.order_by('Last name')
    print my_table

After executing it, you'll get this output:

    +------------+-----------+
    | First name | Last name |
    +------------+-----------+
    |      Renne |      None |
    |     Flávio |   Amieiro |
    |     Álvaro |    Justen |
    +------------+-----------+
    

### Example 5: Reading from CSV and Exporting to HTML

You can export your data to HTML using the plugin HTML (that is shipped by
default with `outputty`). If you don't specify a filename, the HTML plugin
will return a string (encoded with `output_encoding`, specified in
`Table.__init__`). If it receives the filename, the contents will be saved
into it and it'll return nothing.

If you have this code, like in `examples/5_table_to_html_file.py`: 
        
    from outputty import Table
    
    my_table = Table()
    my_table.read('csv', 'nice-software.csv')
    my_table.write('html', 'nice-software.html')

The file `nice-software.html` will be created with this content:

    <table>
      <thead>
        <tr class="header">
          <th>id</th>
          <th>name</th>
          <th>website</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd">
          <td>1</td>
          <td>Python</td>
          <td>http://www.python.org/</td>
        </tr>
        <tr class="even">
          <td>2</td>
          <td>OpenSSH</td>
          <td>http://www.openssh.com/</td>
        </tr>
        <tr class="odd">
          <td>3</td>
          <td>fabric</td>
          <td>http://fabfile.org/</td>
        </tr>
      </tbody>
    </table>

### Example 6: Creating Histograms

There is a plugin called `histogram` that is shipped by default with
`outputty` - it can create histograms of your table's columns (using `numpy`).
The output will be the histogram represented as text.

If you have this code, like in `examples/6_histogram.py`: 
        
    from numpy.random import normal
    from numpy.random import seed
    from outputty import Table
    
    seed(1234)
    distribution = normal(size=1000)
    my_table = Table(headers=['numbers'])
    my_table.extend([[value] for value in distribution])
    print 'Vertical:'
    print my_table.write('histogram', 'numbers', 'vertical', bins=10, height=7)
    print
    print 'Horizontal:'
    print my_table.write('histogram', 'numbers', 'horizontal', bins=10, height=7,
                         character='#')

After executing it, you'll get this output:

    Vertical:
    265      |
             |
            |||
            |||
            ||||
           |||||
          |||||||
    -3.56          2.76
    
    Horizontal:
                  265
    
    -3.56:
    -2.93:
    -2.30: #
    -1.67: ##
    -1.03: #####
    -0.40: #######
    0.23 : #####
    0.87 : ###
    1.50 : #
    2.13 :
    

### Example 7: Using table columns

You can get a entire table column just getting the item `column-name` in table
object. You can also delete an entire column (but you can't actually change an
entire column).

If you have this code, like in `examples/7_table_columns.py`: 
        
    from outputty import Table
    table = Table(headers=['spam', 'eggs', 'ham'])
    table.append(['python', 3.14, 1 + 5j])
    table.append(['rules', 42, 3 + 4j])
    del table['eggs']
    print 'Table after deleting "eggs" column:'
    print table
    print '\nNow only column "spam":'
    print table['spam']

After executing it, you'll get this output:

    Table after deleting "eggs" column:
    +--------+--------+
    |  spam  |  ham   |
    +--------+--------+
    | python | (1+5j) |
    |  rules | (3+4j) |
    +--------+--------+
    
    Now only column "spam":
    [u'python', u'rules']
    


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
