#!/usr/bin/env python2

import optparse
import os
import sys

from corpus.models import Language

optionParser = optparse.OptionParser(usage="%s <options> <document>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-i", "--id", dest="id", help="language id (2 characters)", metavar="ID")
optionParser.add_option("-l", "--language", dest="language", help="language name", metavar="LANG")
(options, args) = optionParser.parse_args()

if not options.id:
    optionParser.error("No language id given")
if not options.language:
    optionParser.error("No language name given")

log = sys.stdout

foundLanguage = Language.objects.filter(id=options.id)
if foundLanguage:
    sys.stderr.write("Error: language \"%s\" already exists in the database (as %s)\n" % (options.id, foundLanguage[0].humanReadable))
else:
    l = Language(id=options.id, humanReadable=options.language)
    l.save()
    log.write("Language %s => %s added to the database\n" % (l.id, l.humanReadable))
