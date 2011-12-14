outputty
========

With `outputty` you can show the data of your Python software in text mode
(terminal, CSV or TXT) in a easy and beautiful way.

By now we have only the classes `Table` and `Histogram` (more to be added).


Installation
------------

Just copy the file `outputty.py` in some path you can do `import outputty`
(sorry for that - it'll be available in PyPI soon).


Examples
--------

### Example 1 -- `Table`

A `Table` made with `dict`-like, `list`-like and `tuple`-like objects. For
example, this code:

    #!/usr/bin/env python
    # coding: utf-8

    from outputty import Table
    my_table = Table(headers=['First name', 'Last name'])
    my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
    my_table.rows.append(('Flávio', 'Amieiro'))
    print my_table

...will produce:

    +------------+-----------+
    | First name | Last name |
    +------------+-----------+
    |     Álvaro |    Justen |
    |     Flávio |   Amieiro |
    +------------+-----------+

And if do you want to access all table rows as dicts, just convert it:

    rows = my_table.to_list_of_dicts()
    print rows[1]['First name']

...and you'll see:

    Flávio


### Example 2 -- `Table.to_csv`

If you want to export your data to CSV (Comma-Separated Values), just execute:

    my_table.to_csv('my-data.csv')

...and see it:


    alvaro@ideas:~/outputty $ cat my-data.csv
    "First name","Last name"
    "Álvaro","Justen"
    "Flávio","Amieiro"


### Example 3 -- `Table(from_csv=...)` and `Table.to_text_file`

You can also import data from a CSV file and export it to a text file:

    alvaro@ideas:~/outputty $ cat nice-software.csv
    id,name,website
    1,Python,http://www.python.org/
    2,OpenSSH,http://www.openssh.com/
    3,fabric,http://fabfile.org/

The code:

    from outputty import Table
    my_table = Table(from_csv='nice-software.csv')
    my_table.to_text_file('nice-software.txt')

...will produce:

    alvaro@ideas:~/outputty $ cat nice-software.txt
    +----+---------+-------------------------+
    | id |   name  |         website         |
    +----+---------+-------------------------+
    |  1 |  Python |  http://www.python.org/ |
    |  2 | OpenSSH | http://www.openssh.com/ |
    |  3 |  fabric |     http://fabfile.org/ |
    +----+---------+-------------------------+


### Example 4 -- `Table(order_by='header_name'[, ordering='asc|desc'])`

You can specify to order data in your table with the parameters `order_by` and
`ordering`. For example:

    #!/usr/bin/env python
    # coding: utf-8

    from outputty import Table
    my_table = Table(headers=['First name', 'Last name'], order_by='Last name')
    my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
    my_table.rows.append({'First name': 'Renne'})
    my_table.rows.append(('Flávio', 'Amieiro'))
    print my_table

...will produce:

    +------------+-----------+
    | First name | Last name |
    +------------+-----------+
    |     Renne  |           |
    |     Flávio |   Amieiro |
    |     Álvaro |    Justen |
    +------------+-----------+

You can also order data using the method `order_by`. For example:

    from outputty import Table
    my_table = Table(headers=['Programming Languages'])
    my_table.rows.extend([['Python'], ['Bash scripting'], ['C']])
    my_table.order_by('Programming Languages') #ordering = 'asc' by default
    print my_table

...will print:

    +-----------------------+
    | Programming Languages |
    +-----------------------+
    |        Bash scripting |
    |                     C |
    |                Python |
    +-----------------------+


### Example 5 -- `Table.to_html(filename='')`

You can export your data to HTML using the method `to_html`. If you don't pass
any parameter it'll return a string (encoded with `output_encoding`, specified
in `Table.__init__`). But you can pass one parameter: the filename to be saved
with the HTML inside.

The code:

    from outputty import Table
    my_table = Table(from_csv='nice-software.csv')
    my_table.to_html('nice-software.html')


...will create the filename `nice-software.html` with this content:

    <table>
      <tr class="header">
        <th>id</th>
        <th>name</th>
        <th>website</th>
      </tr>
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
    </table>

It automatically puts `header`, `odd` and `even` CSS classes so you can change
the layout of the table without needing to change table's HTML code.


### Example 6 -- `Histogram`

This code:

    from numpy.random import normal
    from numpy.random import seed
    from outputty import Histogram

    seed(1234)
    distribution = normal(size=1000)
    my_histogram = Histogram(distribution, bins=10)
    print 'Vertical:'
    print my_histogram.vertical(15)
    print
    print 'Horizontal:'
    print my_histogram.horizontal(5)


...will produce:

    Vertical:
                          265

    -3.56:
    -2.93:
    -2.30: ||
    -1.67: ||||
    -1.03: ||||||||||
    -0.40: |||||||||||||||
    0.23 : ||||||||||||
    0.87 : ||||||
    1.50 : |||
    2.13 :

    Horizontal:
    265      |
             ||
            |||
            ||||
           ||||||
    -3.56          2.76


> If do you want to see more examples, see `tests/test_*.py`.

> To run these examples, see the folder `examples`.

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


New Features
------------

Yes, there are a lot of features to add (it's just the begining). If do you
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
- Run __all tests__ (`make test`) _before_ pushing
  - To run just one test file, execute `nosetests --with-coverage
    tests/test_your-test-file.py`
  - Try to have a test-coverage of 100%
- Create/update documentation (`README.markdown`/docstrings/man page)


Related Software
----------------

- [fabulous](http://lobstertech.com/fabulous.html)
- [tablib](https://github.com/kennethreitz/tablib)
- [clint](https://github.com/kennethreitz/clint)
- [csvstudio](http://code.google.com/p/csvstudio/)
- [PyTables](http://www.pytables.org/)
