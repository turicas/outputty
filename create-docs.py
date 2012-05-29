#!/usr/bin/env python
# coding: utf-8

import os
from glob import glob
import shlex
import subprocess
import outputty


os.chdir('examples')

def file_contents_indented(filename):
    fp = open(filename)
    file_lines = fp.readlines()
    fp.close()
    return ''.join(['    ' + x for x in file_lines])

def execute(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.wait()
    return process.stdout.read()

examples = [x for x in glob('*.py') if x[0].isdigit()]
examples.sort()
example_list = []
for example_filename in examples:
    contents = open(example_filename).readlines()[2:]
    title = 'Example ' + example_filename.split('_')[0]
    config = {}
    body = []
    code = []
    while contents[0].startswith('#') and ' = ' in contents[0]:
        info = contents[0].split(' = ', 1)
        config[info[0].split('#')[1].strip()] = info[1]
        contents = contents[1:]
    in_code = False
    for line in contents:
        line = line[:-1]
        if line.startswith('#') and not in_code:
            body.append(line[1:])
        else:
            in_code = True
            code.append('    ' + line)
    code = '\n'.join(code)
    if 'title' in config:
        title += ': ' + config['title']
    title += '~' * len(title) + '\n'
    if 'input' not in config:
        config['input'] = 'code'
    if 'output' not in config:
        config['output'] = 'stdout'

    have_input = False
    for input_ in config['input'].split(','):
        input_ = input_.strip()
        if input_ == 'code':
            body.append('')
            if have_input:
                body.append('and do you have the code below, like in '
                            '``examples/%s``::' % example_filename)
            else:
                body.append('If you have this code, like in '
                            '`examples/%s`::' % example_filename)
            body.append('    ' + code)
        else:
            input_ = input_.replace("'", '')
            body.append('')
            body.append('If you have the file ``%s`` with these contents::' % \
                        input_)
            body.append('')
            body.append(file_contents_indented(input_))
        have_input = True

    output_lines = execute('python ' + example_filename)
    have_output = False
    for output in config['output'].split(','):
        output = output.strip()
        if output == 'stdout':
            body.append('')
            body.append("After executing it, you'll get this output::")
            body.append('')
            fmt = '\n'.join(['    ' + x for x in output_lines.split('\n')])
            body.append(fmt)
        else:
            output_files = output.split(',')
            for output in output_files:
                output = output.strip().replace("'", '').replace('"', '')
                body.append('')
                body.append('The file `%s` will be created with this content::' % \
                            output)
                body.append('')
                body.append(file_contents_indented(output))
        have_output = True
    body = '\n'.join(body)
    example_list.append(title + '\n' + body + '\n')

fp = open('../README-template.rst')
text = fp.read()
fp.close()
new_readme = open('../README.rst', 'w')
text = text.replace('{{INTRO}}', outputty.__doc__)
text = text.replace('{{AUTHORS}}', open('../AUTHORS.rst').read())
new_readme.write(text)
new_readme.close()

tutorial_template = open('../tutorial-template.rst').read()
tutorial_content = tutorial_template.replace('{{EXAMPLES}}',
                                             '\n'.join(example_list))
tutorial = open('../tutorial.rst', 'w')
tutorial.write(tutorial_content)
tutorial.close()
