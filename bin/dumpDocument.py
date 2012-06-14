#!/usr/bin/env python2

import optparse
import os
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s <options> <document>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="Specify language for the document")
(options, args) = optionParser.parse_args()

if len(args) != 1:
    optionParser.error("You have to provide the id of the document to dump")

out = sys.stdout

candidates = models.SourceDocument.objects.filter(customId=args[0])
if not candidates:
    sys.stderr.write("Error: Document does not exist\n")
    sys.exit(1)
if options.language:
    try:
        document = candidates.get(language=options.language)
    except models.SourceDocument.DoesNotExist:
        sys.stderr.write("Error: Document \"%s\" does not exist for language %s\n" % (args[0], options.language))
        sys.exit(1)
else:
    if len(candidates) > 1:
        sys.stderr.write("Error: More than one language available for document %s.\n" % args[0])
        sys.exit(1)
    else:
        document = candidates[0]

sentences = models.Sentence.objects.filter(document=document)
for s in sentences:
    out.write("%s\n" % s.text)
