#!/usr/bin/env python2

import optparse
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="", add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-i", "--id", dest="id", help="corpus id", metavar="ID")
optionParser.add_option("-d", "--description", dest="description", help="corpus description", metavar="TEXT", default="")
(options, args) = optionParser.parse_args()

if not options.id:
    optionParser.error("No corpus id given")
if len(args) == 0:
    optionParser.error("Error: no documents given\n")

log = sys.stdout

try:
    models.Corpus.objects.get(id=options.id)
    sys.stderr.write("Error: corpus \"%s\" already exists in the database\n" % (options.id))
    sys.exit(1)
except models.Corpus.DoesNotExist:
    pass

corpus = models.Corpus(id=options.id, description=options.description)
corpus.save()
for d in args:
    try:
        document = models.Document.objects.get(id=d)
        corpus.documents.add(document)
    except models.Document.DoesNotExist:
        sys.stderr.write("Error: document \"%s\" not found\n" % d)
        corpus.delete()
        sys.exit(1)
corpus.save()
log.write("Corpus \"%s\" added with %d documents.\n" % (corpus.id, len(corpus.documents.all())))
