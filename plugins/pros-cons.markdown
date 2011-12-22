outputty plugins
================

Requirements
------------

- Each plugin should be contained in a separated file;
- outputty should not load all plugins automatically;
- Plugins should not have namespace conflicts;
- Rules for creating new plugins should be easy and not invasive;
- Plugins should be easy to use;
- Should be a standard way (conventions) to create import/export
  functions/methods, like `Table.import` and `plugin_X.import`;
- A plugin should be read-only (only imports data), write-only (only exports)
  or read-write.


Option 1: same-class
--------------------

### Pros

- Easy to use (just call methods);
- Introspection is fine if plugins only create methods `from_X` and `to_X` --
  will be somethig like:
  `import_plugins = [x for x in dir(my_table) if x.startswith('from_')]` and
  `export_plugins = [x for x in dir(my_table) if x.startswith('to_')]`.


### Cons

- What if two plugins have the same method name?
- With 150 plugins and one from/to for each one, we'll end with a Table class
  with more than 300 methods;
- If we don't use a plugin (or many of them), it'll be imported;
- More implicity (sounds like magic). A user can't know when a plugin is
  available or not.


Option 2: many-classes
----------------------

### Pros

- Namespaces instead of monkey-patches, for example:
  `from outputty import plugin_mysql`, `plugin_mysql.export(my_table)`;
- We still can create a function that assembles a new `Table` with the methods
  we want, as `main.py` does in `same-classe`, but here not automatically. For
  example: `myTable = create_table('MySQL', 'CSV')` will return a `Table`
  class with `BaseTable` + `MysqlTable` + `CSVTable` methods;
- Each plugin will be loaded only where needed (but probably in the start of
  file);
- Introspection is fine if plugins only create methods `from_X` and `to_X` --
  will be somethig like:
  `import_plugins = [x for x in dir(my_table) if x.startswith('from_')]` and
  `export_plugins = [x for x in dir(my_table) if x.startswith('to_')]`.

### Cons

- Verbosity:
  - Explicity imports;
  - Overheaded calls for import/export.
- Less intuitive since we won't call a `Table` method (we'll need to call a
  plugin method passing `my_table` as parameter).


Option 3: one-class
-------------------

### Pros

- No namespace problems (`outputty.plugin_X`);
- Plugins can use helper functions/methods/classes/whatever in
  `outputty/plugin_X.py` and it won't be added to `Table`;
- Each plugin will be loaded only when needed (and not in the start of file).

### Cons

- Introspection (know which plugins are available) can be compromised. We can
  fix this creating a `Table.available_plugins` method that will try to import
  each available plugin and return a list with names that were imported
  succesfully, like `['csv', 'mysql', 'show', 'savefile']`.
