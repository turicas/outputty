Tutorial
========

This tutorial have a lot of examples (and some notes/implementation details in
the end). All examples you'll read here are available to you - see `examples`
folder. You can also learn more details about implementation reading the tests
at `tests/test_*.py`.

If you find any kind of bug, error, have a suggestion, doubt or want to
contribute with code or pay me a beer, __please__ [contact
me](https://github.com/turicas). You can follow the development of this code in
[outputty on GitHub](https://github.com/turicas/outputty).

Enjoy! :-)

### Example 1: Basics of `Table`

A `Table` is simply a list of rows. These rows can be represented as
`dict`-like, `list`-like or `tuple`-like objects. Let's create one `Table`
with some rows and print it to stdout.

If you have this code, like in `examples/1_table.py`: 
        
    from outputty import Table
    my_table = Table(headers=['First Name', 'Last Name', 'Main Language'])
    my_table.append({'First Name': 'Álvaro', 'Last Name': 'Justen',
                     'Main Language': 'Python'}) #appending row as dict
    my_table.append(('Flávio', 'Amieiro', 'Python')) #appending row as tuple
    my_table.append(['Flávio', 'Coelho', 'Python']) #appending row as list
    print my_table

After executing it, you'll get this output:

    +------------+-----------+---------------+
    | First Name | Last Name | Main Language |
    +------------+-----------+---------------+
    |     Álvaro |    Justen |        Python |
    |     Flávio |   Amieiro |        Python |
    |     Flávio |    Coelho |        Python |
    +------------+-----------+---------------+
    

### Example 2: Exporting to a CSV File

Using plugins we can import and export `Table` data to CSV (really, to and
from a lot of formats). Let's create a simple table and export it to a CSV
file.

If you have this code, like in `examples/2_table_to_csv.py`: 
        
    from outputty import Table
    
    my_table = Table(headers=['First name', 'Last name'])
    my_table.append({'First name': 'Álvaro', 'Last name': 'Justen'})
    my_table.append(('Flávio', 'Amieiro'))
    my_table.append(['Flávio', 'Coelho'])
    my_table.write('csv', 'my-data.csv')

The file `my-data.csv` will be created with this content:

    "First name","Last name"
    "Álvaro","Justen"
    "Flávio","Amieiro"
    "Flávio","Coelho"


### Example 3: Exporting to a Text File

We can also import data from a CSV file and export it to a text file (using
plugins, again). The data written to the text file will be the same we saw
when executed `print my_table` in Example 1.

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
    

### Example 7: Using table columns and rows

You can get an entire table column just getting the item `column-name` in
your table object. You can also change and delete an entire column.
If the item you get is a string, a column is returned. If it is an integer, a
row is returned (starting from 0). `Table` objects are iterable, so you can
navigate through the rows with a simple `for` loop.

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
    print 'First row:'
    print table[0]
    print 'All rows:'
    for index, row in enumerate(table):
        print '  Row #%d: %s' % (index, row)
    table['ham'] = [1, 2] # Setting new values for this column
    print 'Table after chaning an entire column:'
    print table

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
    First row:
    [u'python', (1+5j)]
    All rows:
      Row #0: [u'python', (1+5j)]
      Row #1: [u'rules', (3+4j)]
    Table after chaning an entire column:
    +--------+-----+
    |  spam  | ham |
    +--------+-----+
    | python |   1 |
    |  rules |   2 |
    +--------+-----+
    

### Example 8: Other `Table` methods

A `Table` is implemented as a list of rows with some methods to use plugins,
ordering and do other things. `Table` have all operations/methods other
Python mutable sequence objects have so you can use slicing,
`Table.extend`, `Table.index`, `Table.count` and so on. The exception is
`sort` (`Table` have `order_by` instead).
Read more:
[mutable sequence operations](http://docs.python.org/library/stdtypes.html#mutable-sequence-types).

> Note: all these methods support `tuple`, `list` or `dict` notations of row.

If you have this code, like in `examples/8_table_methods.py`: 
        
    from outputty import Table
    
    table = Table(headers=['City', 'State', 'Country'])
    table.append(['Três Rios', 'Rio de Janeiro', 'Brazil'])
    table.append(['Niterói', 'Rio de Janeiro', 'Brazil'])
    table.append(['Rio de Janeiro', 'Rio de Janeiro', 'Brazil'])
    table.append(['Porto Alegre', 'Rio Grande do Sul', 'Brazil'])
    table.append(['São Paulo', 'São Paulo', 'Brazil'])
    
    print 'First 3 rows:'
    for row in table[:3]: # Slicing
        print row
    
    #Change the two last rows:
    table[-2:] = [['Junín', 'Buenos Aires', 'Argentina'],
                  ['Ciudad del Este', 'Alto Paraná', 'Paraguay']]
    #Insert a row in the first position, using dict notation:
    table.insert(0, {'City': 'La Paz', 'State': 'La Paz', 'Country': 'Bolivia'})
    print 'New table:'
    print table
    print
    
    table.reverse()
    print 'And the table in the reversed order:'
    print table
    print
    
    popped_row = table.pop()
    rio = ['Rio de Janeiro', 'Rio de Janeiro', 'Brazil']
    table.append(rio) #repeated row
    number_of_rios = table.count(rio)
    index_of_first_rio = table.index(rio)
    table.remove(rio) #remove the first occurrence of this row
    number_of_rows = len(table)
    print 'Popped row:', popped_row
    print 'Number of rows:', number_of_rows
    print 'Count of Rios rows (before remove):', number_of_rios
    print 'Table after pop and remove:'
    print table
    print
    
    #Removing non-brazilian cities:
    del table[:2]
    #Let's change an entire column:
    table['Country'] = ['Brasil', 'Brasil', 'Brasil']
    print 'Column "Country" changed:'
    print table

After executing it, you'll get this output:

    First 3 rows:
    [u'Tr\xeas Rios', u'Rio de Janeiro', u'Brazil']
    [u'Niter\xf3i', u'Rio de Janeiro', u'Brazil']
    [u'Rio de Janeiro', u'Rio de Janeiro', u'Brazil']
    New table:
    +-----------------+----------------+-----------+
    |       City      |     State      |  Country  |
    +-----------------+----------------+-----------+
    |          La Paz |         La Paz |   Bolivia |
    |       Três Rios | Rio de Janeiro |    Brazil |
    |         Niterói | Rio de Janeiro |    Brazil |
    |  Rio de Janeiro | Rio de Janeiro |    Brazil |
    |           Junín |   Buenos Aires | Argentina |
    | Ciudad del Este |    Alto Paraná |  Paraguay |
    +-----------------+----------------+-----------+
    
    And the table in the reversed order:
    +-----------------+----------------+-----------+
    |       City      |     State      |  Country  |
    +-----------------+----------------+-----------+
    | Ciudad del Este |    Alto Paraná |  Paraguay |
    |           Junín |   Buenos Aires | Argentina |
    |  Rio de Janeiro | Rio de Janeiro |    Brazil |
    |         Niterói | Rio de Janeiro |    Brazil |
    |       Três Rios | Rio de Janeiro |    Brazil |
    |          La Paz |         La Paz |   Bolivia |
    +-----------------+----------------+-----------+
    
    Popped row: [u'La Paz', u'La Paz', u'Bolivia']
    Number of rows: 5
    Count of Rios rows (before remove): 2
    Table after pop and remove:
    +-----------------+----------------+-----------+
    |       City      |     State      |  Country  |
    +-----------------+----------------+-----------+
    | Ciudad del Este |    Alto Paraná |  Paraguay |
    |           Junín |   Buenos Aires | Argentina |
    |         Niterói | Rio de Janeiro |    Brazil |
    |       Três Rios | Rio de Janeiro |    Brazil |
    |  Rio de Janeiro | Rio de Janeiro |    Brazil |
    +-----------------+----------------+-----------+
    
    Column "Country" changed:
    +----------------+----------------+---------+
    |      City      |     State      | Country |
    +----------------+----------------+---------+
    |        Niterói | Rio de Janeiro |  Brasil |
    |      Três Rios | Rio de Janeiro |  Brasil |
    | Rio de Janeiro | Rio de Janeiro |  Brasil |
    +----------------+----------------+---------+
    

### Example 9: Appending a column

You can append a column in your `Table` object using the `append_column`
method or just setting an item (`my_table['new-column'] = ...`). You can pass
a list of values or a function to generate the values based on row data.
Let's see how it works - it's quite simple.

If you have this code, like in `examples/9_append_column.py`: 
        
    from outputty import Table
    
    
    table = Table(headers=['Name', 'Creation Year'])
    table.append(['Python', 1991])
    table.append(['Unix', 1969])
    
    #We have the values, so we'll append it:
    table.append_column('Category', ['Programming Language', 'Operating System'])
    #Same effect for this line:
    #table['Category'] = ['Programming Language', 'Operating System']
    
    #We can also generate the values:
    table.append_column('Age', lambda row: 2012 - row[1]) #row is a list
    #Our function can receive row as dict (with `row_as_dict` parameter) and we
    #can insert the column where we want (with `position` parameter):
    table.append_column('First Letter', lambda row: row['Name'][0],
                        row_as_dict=True, position=0) #row is dict
    #...and the result:
    print table

After executing it, you'll get this output:

    +--------------+--------+---------------+----------------------+-----+
    | First Letter |  Name  | Creation Year |       Category       | Age |
    +--------------+--------+---------------+----------------------+-----+
    |            P | Python |          1991 | Programming Language |  21 |
    |            U |   Unix |          1969 |     Operating System |  43 |
    +--------------+--------+---------------+----------------------+-----+
    



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

You'll receive this data encoded with `output_encoding`. If you need it as
unicode just pass `unicode=True` to this method.

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
