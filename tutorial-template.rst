Tutorial
========

This tutorial have a lot of examples (and some notes/implementation details in
the end). All examples you'll read here are available to you - see ``examples``
folder. You can also learn more details about implementation reading the tests
at ``tests/test_*.py``.

If you find any kind of bug, error, have a suggestion, doubt or want to
contribute with code or pay me a beer, **please**
`contact me <https://github.com/turicas>`_. You can follow the development of
this code in `outputty on GitHub <https://github.com/turicas/outputty>`_.

Enjoy! :-)

{{EXAMPLES}}


Character Encodings
-------------------

Received strings are decoded using **UTF-8** and output is encoded also using
**UTF-8** by default. You can change this behaviour with the parameters
``input_encoding`` and ``output_encoding`` to ``Table``, for example::

    my_table = Table(headers=['Column 1', 'Column 2'], input_encoding='iso-8859-1',
                     output_encoding='utf16')

You can also get the table string decoded, in unicode::

    table_in_unicode = unicode(my_table)

.. See `Standard Encodings in Python <http://docs.python.org/library/codecs.html#standard-encodings>`_
   to get a complete list of the supported encodings.

.. ``headers`` must be a list of strings.


Notes About Data Normalization
------------------------------

We have two kinds of normalization in ``Table``:

- ``.normalize_types()``: used by default when importing from CSV, this method
  convert table rows to the types it identify. All data that in first moment
  are strings will be converted to ``unicode``, ``int``, ``float``,
  ``datetime.date`` or ``datetime.datetime`` when identified.

.. If you want all your data as ``unicode`` when importing from CSV you can
   pass ``convert_types=False`` to ``Table`` so it won't use
   ``normalize_types`` after importing data (it'll just decode your strings
   using ``input_encoding``).

- ``unicode`` normalization: all operations in ``Table`` (import from some format,
  output table in some format, normalization and ordering) will convert data
  internally to ``unicode`` using ``input_encoding`` as codec (passed in
  ``Table.__init__``). When ``convert_types=False``, all row's values will be
  ``unicode``, otherwise only types identified as string will be converted to
  ``unicode``.


``to_list_of_dicts`` and ``to_dict``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to access all table rows as dicts, just convert it using the
method ``to_list_of_dicts``. Using the same table from Example 1, if we
execute::

    rows = my_table.to_list_of_dicts()
    print rows[1]['First Name']

...it'll print::

    Flávio

You'll receive this data encoded with ``output_encoding``. If you need it as
unicode just pass ``unicode=True`` to this method.

You can also convert your table to a ``dict``, with header names as keys and
columns as values and filter which columns will go to the dictionary::

    table_dict = my_table.to_dict()
    print table_dict

    table_dict_filtered = my_table.to_dict(only=['First Name', 'Last Name'])
    print table_dict_filtered

...will print::

    {'Last Name': (u'Justen', u'Amieiro'), 'First Name': (u'\xc1lvaro', u'Fl\xe1vio'), 'Main Language': (u'Python', u'Python')}
    {'Last Name': (u'Justen', u'Amieiro'), 'First Name': (u'\xc1lvaro', u'Fl\xe1vio')}

And if you want to create a ``dict`` with some column value as key and other
column value as value you can specify ``key`` and ``value`` parameters, as in::

    other_table = Table(headers=['date', 'measure'])
    other_table.append(('2011-12-01', 21))
    other_table.append(('2011-12-02', 42))
    other_table.append(('2011-12-03', 3.14))
    other_table.append(('2011-12-04', 2.71))
    values_as_dict = other_table.to_dict(key='date', value='measure')
    print values_as_dict

...that produces::

    {'2011-12-04': 2.71, '2011-12-03': 3.14, '2011-12-02': 42, '2011-12-01': 21}
