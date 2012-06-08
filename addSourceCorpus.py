#!/usr/bin/env python2

import optparse
import os.path
import sys

from corpus.models import Document,Sentence,Language

optionParser = optparse.OptionParser(usage="usage: %prog -l LANG [options] corpus")
optionParser.add_option("-l", "--language", dest="language", help="source language (required)", metavar="LANG")
optionParser.add_option("-i", "--id", dest="id", help="id of the corpus (if not given, the filename will be taken",
                  metavar="ID")
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

if Document.objects.filter(id=options.id):
    sys.stderr.write("Error: document \"%s\" already exists in the database!\n" % options.id)
else:
    languageQuery = Language.objects.filter(id=options.language)
    if not languageQuery:
        sys.stderr.write("Error: language \"%s\" not found in the database!\nYou can add languages with the addLanguage.py command\n" % options.language)
    else:
        language = languageQuery[0]
        fp = open(args[0])
        log.write("Importing corpus \"%s\" from %s (language: %s)...\n" % (options.id, args[0], language.humanReadable))
        d = Document(id=options.id, sourceLanguage=language)
        d.save()
        sentenceId = 1
        for l in fp:
            d.sentence_set.create(id="%s-%d" % (options.id, sentenceId), text=l)
            sentenceId += 1
        d.save()
        log.write("Corpus \"%s\" stored in database with %d sentences.\n" % (d.id, len(d.sentence_set.all())))
