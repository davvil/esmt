#!/usr/bin/env python2

import optparse
import os
import sys

from corpus.models import TranslationSystem

optionParser = optparse.OptionParser(usage="%s <options> <document>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
(options, args) = optionParser.parse_args()

if not args:
    optionParser.error("No system given")
if len(args) > 1:
    optionParser.error("Too many systems given")

log = sys.stdout

try:
    TranslationSystem.get(id=args[0])
    sys.stderr.write("Error: system \"%s\" already exists in the database\n" % args[0])
    sys.exit(1)
except:
    s = TranslationSystem(id=args[0])
    s.save()
    log.write("System %s added to the database\n" % s.id)
