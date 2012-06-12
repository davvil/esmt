#!/usr/bin/env python2

import optparse
import os
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s <options> <document>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
(options, args) = optionParser.parse_args()

if len(args) != 1:
    optionParser.error("You have to provide the id of the document to dump")

out = sys.stdout

try:
    d = models.Document.objects.get(id=args[0])
    sentences = models.Sentence.objects.filter(document = d)
    for s in sentences:
        out.write("%s\n" % s.text)
except models.Document.DoesNotExist:
    sys.stderr.write("Error: Document does not exist\n")
    sys.exit(1)
