#!/usr/bin/env python2

import optparse
import os.path
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="", add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="target language (required)", metavar="LANG")
optionParser.add_option("-i", "--id", dest="id", help="id of the source corpus", metavar="ID")
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
if not options.system:
    optionParser.error("No system given")

log = sys.stdout

try:
    corpus = models.Corpus.objects.get(customId=options.id)
except models.Document.DoesNotExist:
    sys.stderr.write("Error: corpus \"%s\" does not exist in the database!\n" % options.id)
    sys.exit(1)
try:
    language = models.Language.objects.get(id=options.language)
except models.Language.DoesNotExist:
    sys.stderr.write("Error: language \"%s\" not found in the database!" % options.language)
    sys.exit(1)
try:
    system = models.TranslationSystem.objects.get(id=options.system)
except models.TranslationSystem.DoesNotExist:
    sys.stderr.write("Error: system \"%s\" not found in the database!" % options.system)
    sys.exit(1)
    
campaign = None
if options.campaign:
    try:
        campaign = models.EvaluationCampaign.objects.get(id=options.campaign)
    except models.EvaluationCampaign.DoesNotExist:
        sys.stderr.write("Error: Campaign \"%s\" not found in the database!\n" % options.campaign)
        sys.exit(1)

log.write("Importing translations for \"%s\" from %s (language: %s)...\n" % (options.id, args[0], language.humanReadable))
fp = open(args[0])
document2corpuses = models.Document2Corpus.objects.filter(corpus=corpus)
for d2c in document2corpuses:
    sourceDocument = d2c.document
    translatedDocument = models.TranslatedDocument(source=sourceDocument,system=system,language=language)
    if campaign:
        translatedDocument.campaign = campaign
    translatedDocument.save()
    sentences = models.SourceSentence.objects.filter(document = d2c.document)
    for s in sentences:
        l = fp.readline().strip()
        translation = models.Translation(sourceSentence=s, text=l, document=translatedDocument)
