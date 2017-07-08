#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: versioner.py
# Author: Anicka Burova <anicka.burova@gmail.com>
# Date: 07.07.2017
# Last Modified Date: 08.07.2017
# Last Modified By: Anicka Burova <anicka.burova@gmail.com>
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# versioner.py
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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: versioner.py
# Author: Anicka Burova <anicka.burova@gmail.com>
# Date: 07.07.2017
# Last Modified Date: 07.07.2017
# Last Modified By: Anicka Burova <anicka.burova@gmail.com>
#!/bin/env python

import sys
from optparse import OptionParser
import os

import re


usage = "usage: %prog [options] file"
version = "0.2.0.0"
version_text = "%prog {}".format(version)
opt = OptionParser(usage = usage, version = version_text)
opt.add_option  ("-l","--language"
                ,action = "store"
                ,dest = "language", default = 0
                ,help = "manualy select the language")
opt.add_option  ("-s","--show"
                ,action = "store_true"
                ,dest = "show", default = False
                ,help = "show the current version of the file")

opt.add_option  ("","--major"
                ,action = "store_true"
                ,dest = "major", default = False
                ,help = "upgrade major version")
opt.add_option  ("","--minor"
                ,action = "store_true"
                ,dest = "minor", default = False
                ,help = "upgrade minor version")
opt.add_option  ("","--maintenance","--main"
                ,action = "store_true"
                ,dest = "maintenance", default = False
                ,help = "upgrade maintenance version")
opt.add_option  ("","--build"
                ,action = "store_true"
                ,dest = "build", default = False
                ,help = "upgrade build version")
opt.add_option  ("-e","--no-error"
                ,action = "store_true"
                ,dest = "no_error", default = False
                ,help = "no version is not considered as error")
opt.add_option  ("-v","--version-only"
                ,action = "store_true"
                ,dest = "version_only", default = False
                ,help = "if showing, show only the current version")

(options, args) = opt.parse_args()

class Language:
    Unknown, Python, Haskell, Cpp, Rust = range(0,5)

    @staticmethod
    def languages():
        l = []
        for a in dir(Language):
            if not "__" in a and not a in ["parse", "languages", "Unknown"]:
                l.append(a)
        return ", ".join(l)

    @staticmethod
    def parse( text ):
        text = text.lower()
        d = {
            "python" : Language.Python,
            "haskell" : Language.Haskell,
            "cpp"   : Language.Cpp,
            "rust"  : Language.Rust,
        }
        if text in d:
            return d[text]
        for k,v in d.iteritems():
            if text in k:
                return v

        return Language.Unknown

try:
    options.file_path = args[0]
except:
    # try .versionrc file
    try:
        with open(".versionrc", "r") as f:
            m = re.compile("MAIN_VERSION_FILE=(.*)").match(f.read())
            if m:
                options.file_path = m.group(1)
            else:
                raise "no file path"
    except:
        sys.stderr.write("No input file!\n")
        exit(2)

if not os.path.isfile(options.file_path):
    sys.stderr.write("{} not exists!\n".format(options.file_path))
    exit(3)


if options.language:
    lan = Language.parse(options.language)
    if lan == Language.Unknown:
        sys.stderr.write("Incorrect language, available languages: {}\n".format(Language.languages()))
        exit(1)
    options.language = lan
else:
    if options.file_path == "Cargo.toml":
        options.language = Language.Rust
    else:
        _, ext = os.path.splitext(options.file_path)
        exts = {
            ".py" : Language.Python,
            ".cabal" : Language.Haskell,
            ".hpp" : Language.Cpp,
            ".cpp" : Language.Cpp,
        }
        options.language = exts.get(ext, Language.Unknown)

if options.language == Language.Unknown:
    sys.stderr.write("Unknown language, cannot parse the file\n")
    if options.no_error:
        exit(0)
    exit(4)


program_version_re = {
    Language.Python     : re.compile("version\s*=\s*\"(\d+)\.(\d+)\.(\d+).(\d+)\""),
    Language.Cpp        : re.compile("string\s+version\s*=\s*\"(\d+)\.(\d+)\.(\d+).(\d+)\""),
    Language.Haskell    : re.compile("version\s*:\s*(\d+)\.(\d+)\.(\d+).(\d+)"),
    Language.Rust       : re.compile("version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\""),
}

program_version_update = {
    Language.Python     : "version = \"{}.{}.{}.{}\"",
    Language.Cpp        : "string version = \"{}.{}.{}.{}\"",
    Language.Haskell    : "version:             {}.{}.{}.{}",
    Language.Rust       : "version = \"{}.{}.{}\"",
}

def get_version(options):
    program_re = program_version_re[options.language]
    with open(options.file_path,"r") as f:
        lines = f.readlines()
        for line in lines:
            m = program_re.match(line)
            if m and m.groups == 4:
                return (m.group(0), int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)))
            elif m:
                return (m.group(0), int(m.group(1)),int(m.group(2)),int(m.group(3)),0)
    return None



current_version = get_version(options)
old_version = current_version
if not current_version:
    if options.no_error:
        exit(0)
    else:
        exit(10)
upgraded = False

if options.major:
    t,m,_,_,_ = current_version
    current_version = (t, m + 1, 0, 0, 0)
    upgraded = True

if options.minor:
    t,m,n,_,_ = current_version
    current_version = (t, m , n + 1, 0, 0)
    upgraded = True

if options.maintenance:
    t,m,n,a,_ = current_version
    current_version = (t, m , n, a + 1, 0)
    upgraded = True

if options.build:
    t,m,n,a,b = current_version
    current_version = (t, m , n, a, b + 1)
    upgraded = True


if options.show:
    _,m,n,a,b = current_version
    _,om,on,oa,ob = old_version
    if options.version_only:
        sys.stderr.write("{}.{}.{}.{}\n".format(m,n,a,b))
    else:
        if upgraded:
            sys.stderr.write("Version has been upgraded from '{}.{}.{}.{}' to '{}.{}.{}.{}'\n".format(om,on,oa,ob,m,n,a,b))
        else:
            sys.stderr.write("Current version is '{}.{}.{}.{}'\n".format(m,n,a,b))
    exit(0)

orig, major, minor, maintenance, build = current_version

updated = program_version_update[options.language].format(major, minor, maintenance, build)

text = None
with open(options.file_path,"r") as f:
    text = f.read()

text = text.replace(orig, updated)

if upgraded:
    _,m,n,a,b = current_version
    _,om,on,oa,ob = old_version
    sys.stderr.write("Version has been upgraded from '{}.{}.{}.{}' to '{}.{}.{}.{}'\n".format(om,on,oa,ob,m,n,a,b))

sys.stdout.write(text)
