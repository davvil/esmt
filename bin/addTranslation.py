#!/usr/bin/env python2

import optparse
import os.path
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="", add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="target language (required)", metavar="LANG")
optionParser.add_option("-i", "--id", dest="id", help="id of the source document",
                  metavar="ID")
optionParser.add_option("-s", "--system", dest="system", help="system id")
optionParser.add_option("--campaign", dest="campaign", help="evaluation campaign for this document", metavar="ID")
(options, args) = optionParser.parse_args()

if len(args) == 0:
    optionParser.error("You have to give a file to import data from")
if len(args) > 1:
    optionParser.error("Importing more than one translation at a time is not supported yet")
if not options.language:
    optionParser.error("No language given")
if not options.id:
    optionParser.error("No document id given")

log = sys.stdout

try:
    models.Corpus.objects.get(id=options.id):
except models.Document.DoesNotExist:
    sys.stderr.write("Error: corpus \"%s\" does not exist in the database!\n" % options.id)
    sys.exit(1)
try:
    language = models.Language.objects.get(id=options.language)
except models.Language.DoesNotExist:
    sys.stderr.write("Error: language \"%s\" not found in the database!" % options.language)
    sys.exit(1)
campaign = None
if options.campaign:
    try:
        campaign = models.EvaluationCampaign.objects.get(id=options.campaign)
        d.campaigns.add(campaign)
    except models.EvaluationCampaign.DoesNotExist:
        sys.stderr.write("Error: Campaign \"%s\" not found in the database!\n" % options.campaign)
        sys.exit(1)

fp = open(args[0])
log.write("Importing translations for \"%s\" from %s (language: %s)...\n" % (options.id, args[0], language.humanReadable))

        sentenceId = 1
        for l in fp:
            d.sentence_set.create(id="%s-%d" % (options.id, sentenceId), text=l)
            sentenceId += 1
        d.save()
        log.write("Document \"%s\" stored in database with %d sentences.\n" % (d.id, len(d.sentence_set.all())))
        if not options.noCorpus:
            c = models.Corpus(id=options.id)
            c.save()
            c.documents.add(d)
            c.save()
            log.write("Created corpus \"%s\" with this document.\n" % options.id)
