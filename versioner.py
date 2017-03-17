import sys
from optparse import OptionParser
import os


usage = "usage: %prog [options] file"
program_version = "0.1.0"
version = "%prog {}".format(program_version)
opt = OptionParser(usage = usage, version = version)
opt.add_option  ("-l","--language"
                ,action = "store"
                ,dest = "language", default = 0
                ,help = "manualy select the language")

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
        ".hs" : Language.Haskell,
        ".hpp" : Language.Cpp,
        ".cpp" : Language.Cpp,
    }
    options.language = exts.get(ext, Language.Unknown)

if options.language == Language.Unknown:
    sys.stderr.write("Unknown language, cannot parse the file")
    exit(4)


print (options)

