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
    my_table.rows.append(['Tatiana', 'Al-Chueyr'])
    my_table.rows.append(('Flávio', 'Amieiro'))
    print my_table

...will produce:

    +------------+-----------+
    | First name | Last name |
    +------------+-----------+
    |     Álvaro |    Justen |
    |    Tatiana | Al-Chueyr |
    |     Flávio |   Amieiro |
    +------------+-----------+


### Example 2 -- `Table.to_csv`

If you want to export your data to CSV (Comma-Separated Values), just execute:

    my_table.to_csv('my-data.csv')

...and see it:


    alvaro@ideas:~/outputty $ cat my-data.csv 
    "First name","Last name"
    "Álvaro","Justen"
    "Tatiana","Al-Chueyr"
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


### Example 4 -- `Histogram`

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

> To run these examples, see the folder `samples`.

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
