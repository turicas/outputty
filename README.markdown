outputty
========

With `outputty` you can show the data of your Python software in text mode
(terminal, CSV or TXT) in a easy and beautiful way.

By now we have only the class `Table` (in future we'll add progress bar,
histogram and more).


Installation
------------

Just copy the file `outputty.py` in some path you can do `import outputty`
(sorry for that - it'll be available in PyPI soon).


Examples
--------

### Example 1

A `Table` made with `dict`, `list` and `tuple`. This code:

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


### Example 2

If you want to export your data to CSV (Comma-Separated Values), just execute:

    my_table.to_csv('my-data.csv')

...and see it:


    alvaro@ideas:~/outputty $ cat my-data.csv 
    "First name","Last name"
    "Álvaro","Justen"
    "Tatiana","Al-Chueyr"
    "Flávio","Amieiro"


### Example 3

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


> If you want to see more examples, see `tests/test_Table.py`.


Type Of Data and Encodings
--------------------------

`outputty` will try to convert every element inside a row to `unicode`. In
strings it'll use `string.decode(input_encoding)`, where `input_encoding` is
specified in `Table.__init__`. For other types (integer, float etc.) it'll use
`unicode(element)`.

Input strings will be decoded using __UTF-8__ and output will be encoded using
__UTF-8__ by default. You can change this behaviour passing the parameters
`input_encoding` and `output_encoding` to `Table`, for example:

    my_table = Table(headers=['First', 'Last'], input_encoding='iso-8859-1',
                     output_encoding='utf16')

You can also get the table string decoded, in unicode:

    table_in_unicode = unicode(my_table)


New Features
------------

Yes, there are a lot of features to add (it's just the begining). If do you
want to contribute, please see our
[WISHLIST.markdown](https://github.com/turicas/outputty/blog/master/WISHLIST.markdown)
file.

You can also use the [Github Issue Tracking
System](https://github.com/turicas/outputty/issues) - it's up to you.
