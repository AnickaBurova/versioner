import sys
from optparse import OptionParser


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

if options.language:
    lan = Language.parse(options.language)
    if lan == Language.Unknown:
        sys.stderr.write("Incorrect language, available languages: {}".format(Language.languages()))
        exit(1)
    options.language = lan


print (options)

