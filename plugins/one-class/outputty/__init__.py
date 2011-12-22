#!/usr/bin/env python

class Table(object):
    def __init__(self, data=None):
        self.data = data or [5, 4, 3, 2, 1]
        self.plugins = {}

    def _load_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            complete_name = 'outputty.plugin_' + plugin_name
            plugin = __import__(complete_name, fromlist=['outputty'])
            self.plugins[plugin_name] = plugin
        return self.plugins[plugin_name]

    def sort(self):
        self.data.sort()

    def read(self, plugin_name, *args, **kwargs):
        plugin = self._load_plugin(plugin_name)
        plugin.read(self, *args, **kwargs)

    def write(self, plugin_name, *args, **kwargs):
        plugin = self._load_plugin(plugin_name)
        plugin.write(self, *args, **kwargs)
