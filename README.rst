outputty
========

``outputty`` is a simple Python library that helps you importing, filtering
and exporting data. It is composed by a main ``Table`` class and a lot of
plugins that helps importing and exporting data to/from ``Table``.

You can write your own plugin easily (see ``outputty/plugin_*.py`` for
examples). Some examples of plugins are: CSV, text, HTML and histogram.


Installation
------------

As simple as executing::

    pip install outputty


Note: as ``pip`` tries to compile everything and ``outputty`` depends on
``MySQL-Python`` package (which needs compilation), you need to have
libmysqlclient's headers, compilers and related stuff. To install it on
Debian/Ubuntu, just execute::

    apt-get install build-essential libmysqlclient-dev


Example
-------

Code time!::

    >>> from outputty import Table
    >>> my_table = Table(headers=['name', 'age']) # headers are the columns
    >>> my_table.append(('Álvaro Justen', 24)) # a row as tuple
    >>> my_table.append({'name': 'Other User', 'age': 99}) # a row as dict
    >>> print my_table # a text representation of Table
    +---------------+-----+
    |      name     | age |
    +---------------+-----+
    | Álvaro Justen |  24 |
    |    Other User |  99 |
    +---------------+-----+

    >>> print 'First row:', my_table[0] # Table is indexable
    First row: [u'\xc1lvaro Justen', 24]

    >>> print 'Sum of ages:', sum(my_table['age']) # you can get columns too
    Sum of ages: 123

    >>> my_table.write('csv', 'my-table.csv') # CSV plugin will save its contents in a file
    >>> # let's see what's in the file...
    >>> print open('my-table.csv').read()
    "name","age"
    "Álvaro Justen","24"
    "Other User","99"

    >>> # let's use HTML plugin!
    >>> print my_table.write('html') # without filename ``write`` will return a string
    <table>
      <thead>
        <tr class="header">
          <th>name</th>
          <th>age</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd">
          <td>Álvaro Justen</td>
          <td>24</td>
        </tr>
        <tr class="even">
          <td>Other User</td>
          <td>99</td>
        </tr>
      </tbody>
    </table>


``Table`` have **a lot** of other features. To learn more (by examples), read
`outputty tutorial <https://github.com/turicas/outputty/blob/master/tutorial.rst>`_
and see ``examples`` folder. Enjoy!


New Features
------------

Yes, there are a lot of features to add (it's just the begining). If you
want to contribute, please see our
`outputty wishlist <https://github.com/turicas/outputty/blob/master/WISHLIST.rst>`_.

You can also use the `outputty Issue Tracking System on GitHub <https://github.com/turicas/outputty/issues>`_
to report bugs.


Contributing
------------

If you want to contribute to this project, please:

- Install dependencies for development running ``pip install -r requirements/development.txt``.
- Execute ``make test`` to run all tests -- please run **all tests** *before*
  pushing.

  - To run just one test file execute:
    ``nosetests --with-coverage --cover-package outputty  tests/test_your-test-file.py``
  - Try to have a test-coverage of 100%.
  - Use `Test-driven development <http://en.wikipedia.org/wiki/Test-driven_development>`_.

- Use `nvie's gitflow <https://github.com/nvie/gitflow>`_ - to learn, read
  `A Successful Git branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_.

- Create/update documentation (README/docstrings/man page)

  - **Do NOT** edit ``README.rst`` and ``tutorial.rst``, edit
    ``README-template.rst`` or ``tutorial-template.rst`` instead and run
    ``make create-docs`` to create the new ``README.rst`` and
    ``tutorial.rst`` (before committing). The tutorial will be created based on
    files in ``examples`` folder.


New Plugins
~~~~~~~~~~~

If you want to create a new plugin to import/export from/to some new
resource, please see files ``outputty/plugin_*.py`` as examples. They are so
simple, please follow these steps:

- Create a file named ``outputty/plugin_name.py``, where ``name`` is the name of
  your plugin.

- Create ``read`` and/or ``write`` functions in this file. These functions receive
  the ``Table`` object and optional parameters.

  - ``read``: should read data from the resource specified in parameters and put
    this data in ``Table`` (using ``Table.append`` or ``Table.extend``).
  - ``write``: should read data from ``Table`` (iterating over it, using slicing
    etc.) and write this data to the resource specified in parameters.

- Call your plugin executing ``my_table.write('name', optional_parameters...)``
  or ``my_table.read('name', optional_parameters...)`` (where ``name`` is your
  plugin's name) - when you execute it ``outputty`` will call
  ``outputty.plugin_name.read``/``outputty.plugin_name.write``.


Encoding and Decoding
+++++++++++++++++++++

Your plugin's ``read`` function **must** put all data inside in unicode and your
plugin's ``write`` function will receive a ``Table`` object with all data in
unicode (it should not change this). But if you need to decode/encode
before/after doing some actions in your plugin, you can use ``Table.decode()``
and ``Table.encode()``.


Contributors
~~~~~~~~~~~~

This software is written and maintained by
`Álvaro Justen <https://github.com/turicas>`_ but received a lot of
contributions. My sincerely thanks to:

- `Fundação Getúlio Vargas <http://www.fgv.br/>`_ for letting me invest my time
  on it.
- `Douglas Andrade <https://github.com/douglas>`_ for showing me
  `textwrap.dedent` and writting more legible tests.
- `Flávio Coelho <https://github.com/fccoelho>`_ for creating `histogram` and
  giving a lot of suggestions.
- `Renne Rocha <https://github.com/rennerocha>`_ for creating `order_by`.
- `Tatiana Al-Chueyr <https://github.com/tatiana>`_ for designing and coding
  architecture proposals and suggestions for the plugin API (including the
  architecture we are using).
- `Flávio Amieiro <https://github.com/flavioamieiro>`_ for a lot of suggestions
  and interpretations about design.



Related Software
----------------

- outputty-like:

    - `tablib <https://github.com/kennethreitz/tablib>`_: format-agnostic tabular
      dataset library.
    - `PyTables <http://www.pytables.org/>`_: package for managing hierarchical
      datasets and designed to efficiently and easily cope with extremely large
      amounts of data.
    - `csvstudio <http://code.google.com/p/csvstudio/>`_: Python tool to analyze
      csv files.
    - `csvsimple <http://pypi.python.org/pypi/csvsimple>`_: a simple tool to
      handle CSV data.
    - `toolshed <http://pypi.python.org/pypi/toolshed>`_: less boiler-plate.
    - `buzhug <http://buzhug.sourceforge.net/>`_: a fast, pure-Python
      database engine.

- Data analysis:

    - `pyf <http://pyfproject.org/>`_: framework and platform dedicated to large
      data processing, mining, transforming, reporting and more.
    - `pygrametl <http://pygrametl.org/>`_: Python framework which offers
      commonly used functionality for development of Extract-Transform-Load
      (ETL) processes.
    - `etlpy <http://sourceforge.net/projects/etlpy>`_ seems to be a dead project.
    - `orange <http://orange.biolab.si/>`_: data visualization and analysis for
      novice and experts.
    - `Ruffus <http://ruffus.org.uk/>`_: lightweight python module to run
      computational pipelines.
    - `webstore <https://github.com/okfn/webstore>`_: web-api enabled datastore
      backed onto sql databases

- Command-line tools:

    - `fabulous <http://lobstertech.com/fabulous.html>`_: library designed to
      make the output of terminal applications look fabulous.
    - `termcolor <http://pypi.python.org/pypi/termcolor>`_: ANSII Color
      formatting for output in terminal.
    - `clint <https://github.com/kennethreitz/clint>`_: Python Command-line
      Application Tools.

- Other:

    - `pyspread <http://manns.github.com/pyspread/>`_: non-traditional
      spreadsheet application.
