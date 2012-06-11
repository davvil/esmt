#!/usr/bin/env python2

import optparse
import os.path
import sys

import corpus.models as models

optionParser = optparse.OptionParser(usage="", add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-l", "--language", dest="language", help="source language (required)", metavar="LANG")
optionParser.add_option("-i", "--id", dest="id", help="id of the document (if not given, the filename will be taken)",
                  metavar="ID")
optionParser.add_option("-u", "--unique-sentence-id", help="create a (hopefully) unique sentence id for each sentence in the corpus", dest="uniqueSentenceId", action="store_true")
optionParser.add_option("-C", "--no-corpus", dest="noCorpus", help="do not create a corpus for this document", action="store_true")
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

if models.Document.objects.filter(id=options.id):
    sys.stderr.write("Error: document \"%s\" already exists in the database!\n" % options.id)
else:
    languageQuery = models.Language.objects.filter(id=options.language)
    if not languageQuery:
        sys.stderr.write("Error: language \"%s\" not found in the database!\nYou can add languages with the addLanguage.py command\n" % options.language)
    else:
        language = languageQuery[0]
        fp = open(args[0])
        log.write("Importing corpus \"%s\" from %s (language: %s)...\n" % (options.id, args[0], language.humanReadable))
        d = models.Document(id=options.id, sourceLanguage=language)
        d.save()
        for (n, l) in enumerate(fp):
            s = d.sentence_set.create(text=l)
            if not options.uniqueSentenceId:
                s.userId = "%d" % (n+1)
            else:
                s.userId = "%s__%d" % (d.id, (n+1))
            s.save()
        d.save()
        log.write("Document \"%s\" stored in database with %d sentences.\n" % (d.id, len(d.sentence_set.all())))
        if not options.noCorpus:
            c = models.Corpus(id=options.id)
            c.save()
            c.documents.add(d)
            c.save()
            log.write("Created corpus \"%s\" with this document.\n" % options.id)
