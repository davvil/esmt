#!/usr/bin/env python2

import optparse
import os
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s <options> <corpus>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="Specify language for the document")
optionParser.add_option("-s", "--sentences", dest="sentences", help="Dump the sentences instead of documents ids", action="store_true")
(options, args) = optionParser.parse_args()

if len(args) != 1:
    optionParser.error("You have to provide the id of the corpus to dump")

out = sys.stdout

candidates = models.Corpus.objects.filter(customId=args[0])
if not candidates:
    sys.stderr.write("Error: Corpus \"%s\" does not exist\n" % args[0])
    sys.exit(1)
if options.language:
    try:
        corpus = candidates.get(language=options.language)
    except models.Corpus.DoesNotExist:
        sys.stderr.write("Error: Corpus \"%s\" does not exist for language %s\n" % (args[0], options.language))
        sys.exit(1)
else:
    if len(candidates) > 1:
        sys.stderr.write("Error: More than one corpus available for document %s.\n" % args[0])
        sys.exit(1)
    else:
        corpus = candidates[0]

document2corpuses = models.Document2Corpus.objects.filter(corpus=corpus)
for d2c in document2corpuses:
    if not options.sentences:
        sys.stdout.write("%s\n" % d2c.document)
    else:
        sentences = models.Sentence.objects.filter(document = d2c.document)
        for s in sentences:
            out.write("%s\n" % s.text)
