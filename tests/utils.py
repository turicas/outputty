#!/usr/bin/env python
# coding: utf-8

# Copyright 2011 Álvaro Justen
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import shlex
import os


TESTS_PATH = os.path.dirname(__file__)
OUTPUTTY_EXECUTABLE = os.path.join(TESTS_PATH, '../outputty-cli')

def sh(command, finalize=True):
    process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if finalize:
        process.wait()
        process.out = process.stdout.read()
        process.err = process.stderr.read()
    return process

def execute(arguments='', stdin=''):
    process = sh(OUTPUTTY_EXECUTABLE + ' ' + arguments, finalize=False)
    process.stdin.write(stdin)
    process.stdin.close()
    process.wait()
    return process.stdout.read(), process.stderr.read()
