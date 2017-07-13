#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: versioner-has-msg.py
# Author: Anicka Burova <anicka.burova@gmail.com>
# Date: 13.07.2017
# Last Modified Date: 13.07.2017
# Last Modified By: Anicka Burova <anicka.burova@gmail.com>
#
# Copyright (c) 2017 Anicka Burova <anicka.burova@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

has_msg = False

for line in sys.stdin.readlines():
    line = line.strip()
    if len(line) > 0 and line[0] != "#":
        has_msg = True
        break

exit(0 if has_msg else 1)
