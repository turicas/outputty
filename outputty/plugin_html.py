#!/usr/bin/env python
# coding: utf-8

def _to_html_unicode(table):
    result = ['<table>', '  <thead>']
    if table.css_classes:
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
        if table.css_classes:
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

def write(table, filename='', css_classes=True):
    table.css_classes = css_classes
    contents = _to_html_unicode(table).encode(table.output_encoding)
    if not filename:
        return contents
    else:
        fp = open(filename, 'w')
        fp.write(contents)
        fp.close()
