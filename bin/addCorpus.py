#!/usr/bin/env python2

import optparse
import os
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s [options] -l LANG -i <ID> <files>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-i", "--id", dest="id", help="corpus id", metavar="ID")
optionParser.add_option("-d", "--description", dest="description", help="corpus description", metavar="TEXT", default="")
optionParser.add_option("-l", "--language", dest="language", help="source language (required)", metavar="LANG")
optionParser.add_option("--campaign", dest="campaign", help="evaluation campaign for this document", metavar="ID")
(options, args) = optionParser.parse_args()

if not options.id:
    optionParser.error("No corpus id given")
if not options.language:
    optionParser.error("No language given")
if len(args) == 0:
    optionParser.error("Error: no documents given\n")

log = sys.stdout

try:
    language = models.Language.objects.get(id=options.language)
except models.Language.DoesNotExist:
    sys.stderr.write("Error: language \"%s\" not found in the database!\n" % options.language)
    sys.exit(1)
try:
    models.Corpus.objects.get(customId=options.id, language=language)
    sys.stderr.write("Error: corpus \"%s\" already exists in the database\n" % (options.id))
    sys.exit(1)
except models.Corpus.DoesNotExist:
    pass

corpus = models.Corpus(customId=options.id, language=language, description=options.description)
corpus.save()
if options.campaign:
    try:
        campaign = models.EvaluationCampaign.objects.get(id=options.campaign)
        corpus.campaigns.add(campaign)
        corpus.save()
    except models.EvaluationCampaign.DoesNotExist:
        sys.stderr.write("Error: Campaign \"%s\" not found\n" % options.campaign)
        sys.exit(1)
for (n, d) in enumerate(args):
    try:
        document = models.SourceDocument.objects.get(customId=d, language=language)
        d2c = models.Document2Corpus(document=document, corpus=corpus, order=n)
        d2c.save()
        #corpus.documents.add(document)
    except models.SourceDocument.DoesNotExist:
        sys.stderr.write("Error: document \"%s\" (language: %s) not found\n" % (d, options.language))
        corpus.delete()
        sys.exit(1)
#corpus.save()
log.write("Corpus \"%s\" added with %d documents.\n" % (corpus, len(corpus.documents.all())))
