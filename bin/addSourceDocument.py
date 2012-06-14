#!/usr/bin/env python2

import optparse
import os.path
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="%s [options] -l LANG <file>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="source language (required)", metavar="LANG")
optionParser.add_option("-i", "--id", dest="id", help="id of the document (if not given, the filename will be taken)",
                  metavar="ID")
optionParser.add_option("-u", "--unique-sentence-id", help="create a (hopefully) unique sentence id for each sentence in the corpus", dest="uniqueSentenceId", action="store_true")
optionParser.add_option("-C", "--no-corpus", dest="noCorpus", help="do not create a corpus for this document", action="store_true")
optionParser.add_option("--campaign", dest="campaign", help="evaluation campaign for this document", metavar="ID")
(options, args) = optionParser.parse_args()

if len(args) == 0:
    optionParser.error("You have to give a file to import data from")
if len(args) > 1:
    optionParser.error("Importing more than one corpus at a time is not supported yet")
if not options.language:
    optionParser.error("No language given")
if not options.id:
    options.id = os.path.basename(args[0])

log = sys.stdout

try:
    language = models.Language.objects.get(id=options.language)
except models.Language.DoesNotExist:
    sys.stderr.write("Error: language \"%s\" not found in the database!\n" % options.language)
    sys.exit(1)

if models.SourceDocument.objects.filter(customId=options.id, language=language):
    sys.stderr.write("Error: document \"%s\" (%s) already exists in the database!\n"
                     % (options.id, language.humanReadable))
    sys.exit(1)

fp = open(args[0])

# Document creation
log.write("Importing corpus \"%s\" from %s (language: %s)...\n" % (options.id, args[0], language.humanReadable))
d = models.SourceDocument(customId=options.id, language=language)
d.save()
campaign = None
if options.campaign:
    try:
        campaign = models.EvaluationCampaign.objects.get(id=options.campaign)
        d.campaigns.add(campaign)
        d.save()
    except models.EvaluationCampaign.DoesNotExist:
        sys.stderr.write("Error: Campaign \"%s\" not found\n" % options.campaign)
        d.delete()
        sys.exit(1)

# Adding the sentences
for (n, l) in enumerate(fp):
    s = d.sentence_set.create(text=l.strip())
    if not options.uniqueSentenceId:
        s.customId = "%d" % (n+1)
    else:
        if campaign:
            s.customId = "%s__%s__%d" % (campaign.id, d.id, (n+1))
        else:
            s.customId = "%s__%d" % (d.id, (n+1))
    s.save()
d.save()
log.write("Document \"%s\" stored in database with %d sentences.\n" % (d.customId, len(d.sentence_set.all())))

# Corpus creation
if not options.noCorpus:
    c = models.Corpus(customId=options.id, language=language)
    c.save()
    if campaign:
        c.campaigns.add(campaign)
        c.save()
    c2d = models.Document2Corpus(document=d, corpus=c, order=0)
    c2d.save()
    log.write("Created corpus \"%s\" with this document.\n" % options.id)
