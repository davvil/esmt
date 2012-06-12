#!/usr/bin/env python2

import optparse
import os
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s <options> <corpus>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-s", "--sentences", dest="sentences", help="Dump the sentences instead of documents ids", action="store_true")
(options, args) = optionParser.parse_args()

if len(args) != 1:
    optionParser.error("You have to provide the id of the corpus to dump")

out = sys.stdout

try:
    c = models.Corpus.objects.get(id=args[0])
    documents = c.documents.all()
    for d in documents:
        if not options.sentences:
            sys.stdout.write("%s\n" % d)
        else:
            sentences = models.Sentence.objects.filter(document = d)
            for s in sentences:
                out.write("%s\n" % s.text)
except models.Corpus.DoesNotExist:
    sys.stderr.write("Error: Corpus does not exist\n")
    sys.exit(1)
