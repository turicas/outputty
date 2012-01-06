#!/usr/bin/env python
# coding: utf-8

def _to_html_unicode(table, css_classes):
    result = ['<table>', '  <thead>']
    if css_classes:
        result.append('    <tr class="header">')
    else:
        result.append('    <tr>')
    for header in table.headers:
        result.append('      <th>%s</th>' % header)
    result.extend(['    </tr>', '  </thead>'])
    if len(table):
        result.append('  <tbody>')
    i = 1
    for row in table:
        if css_classes:
            result.append('    <tr class="%s">' % \
                          ('odd' if i % 2 else 'even'))
        else:
            result.append('    <tr>')
        for value in row:
            if value is None:
                value = ''
            result.append('      <td>%s</td>' % value)
        result.append('    </tr>')
        i += 1
    if len(table):
        result.append('  </tbody>')
    result.append('</table>')
    return '\n'.join(result)

def write(table, filename_or_pointer=None, css_classes=True):
    contents = _to_html_unicode(table, css_classes) + '\n'
    contents = contents.encode(table.output_encoding)
    if not filename_or_pointer:
        return contents
    else:
        if isinstance(filename_or_pointer, (str, unicode)):
            fp = open(filename_or_pointer, 'w')
            close = True
        else:
            fp = filename_or_pointer
            close = False
        fp.write(contents)
        if close:
            fp.close()
