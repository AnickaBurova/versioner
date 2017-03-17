import sys
from optparse import OptionParser
import os

import re


usage = "usage: %prog [options] file"
program_version = "0.1.0"
version = "%prog {}".format(program_version)
opt = OptionParser(usage = usage, version = version)
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
opt.add_option  ("","--build"
                ,action = "store_true"
                ,dest = "build", default = False
                ,help = "upgrade build version")

(options, args) = opt.parse_args()

class Language:
    Unknown, Python, Haskell, Cpp = range(0,4)

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
    sys.stderr.write("No input file!")
    exit(2)

if not os.path.isfile(options.file_path):
    sys.stderr.write("{} not exists!".format(options.file_path))
    exit(3)


if options.language:
    lan = Language.parse(options.language)
    if lan == Language.Unknown:
        sys.stderr.write("Incorrect language, available languages: {}".format(Language.languages()))
        exit(1)
    options.language = lan
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
    sys.stderr.write("Unknown language, cannot parse the file")
    exit(4)


program_version_re = {
    Language.Python     : re.compile("program_version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\""),
    Language.Cpp        : re.compile("string\s+program_version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\""),
    Language.Haskell    : re.compile("version\s*:\s*(\d+)\.(\d+)\.(\d+)"),
}

program_version_update = {
    Language.Python     : "program_version = \"{}.{}.{}\"",
    Language.Cpp        : "string program_version = \"{}.{}.{}\"",
    Language.Haskell    : "version:             {}.{}.{}",
}

def get_version(options):
    program_re = program_version_re[options.language]
    with open(options.file_path,"r") as f:
        lines = f.readlines()
        for line in lines:
            m = program_re.match(line)
            if m:
                return (m.group(0), int(m.group(1)),int(m.group(2)),int(m.group(3)))
    return None



current_version = get_version(options)

if options.major:
    t,m,_,_ = current_version
    current_version = (t, m + 1, 0, 0)

if options.minor:
    t,m,n,_ = current_version
    current_version = (t, m , n + 1, 0)

if options.build:
    t,m,n,b = current_version
    current_version = (t, m , n, b + 1)

if options.show:
    print (current_version[0])
    print ("{}.{}.{}".format(current_version[1],current_version[2],current_version[3]))
    exit(0)

orig, major, minor, build = current_version

updated = program_version_update[options.language].format(major, minor, build)

text = None
with open(options.file_path,"r") as f:
    text = f.read()

text = text.replace(orig, updated)

print (text)
