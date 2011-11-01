outputty
========

With `outputty` you can show the data of your Python software in text mode
(terminal, CSV or TXT) in a easy and beautiful way.


Installation
------------

For now, just copy the file `outputty.py` in some path you can use it with
`import outputty`. We'll add it to PyPI soon.


Examples
--------

By now we have only the class `Table` (in future we'll add progress bar,
histogram and more). We don't have docstrings yet, sorry. If you want to see
more examples, just open `tests/test_Table.py` in your favorite code editor.
:-)

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


Type Of Data
------------

Every element inside a row will be transformed to
`unicode` -- you can use integers, float etc.

Input strings will be decoded using __UTF-8__ and output will be encoded using
__UTF-8__ by default. You can change this behaviour passing the parameters
`input_codec` and `output_codec` to `Table`, for example:

    my_table = Table(headers=['First', 'Last'], input_codec='iso8859-1',
    output_codec='utf16')


To Do
-----

There are a lot of features to add. If you want to contribute, please see the
`TODO` file -- I'll put there the list of next features. You can use the
GitHub's issue tracking too.
