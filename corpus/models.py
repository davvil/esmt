from django.db import models

################################################################################
# We will organzie most of the material in "Evaluation Campaigns",
# e.g. "WMT2012", "TaraXU R2", etc.
class EvaluationCampaign(models.Model):
    id = models.CharField(primary_key = True, max_length = 200)
    description = models.TextField()

    def __unicode__(self):
        return self.id

################################################################################
# These classes are mainly for consistency in terminology
class Language(models.Model):
    id = models.CharField(primary_key = True, max_length = 2)
    humanReadable = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.humanReadable

# These are very generic identifiers for systems, specifics should be
# added in the description of the translations
class TranslationSystem(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    def __unicode__(self):
        return self.id

################################################################################
# The basic unit for containing sentences to translate. The documents
# will afterwards be grouped into corpora (see below).
class Document(models.Model):
    language = models.ForeignKey(Language)
    campaigns = models.ManyToManyField("EvaluationCampaign")

# A document that is to be translated
class SourceDocument(Document):
    customId = models.CharField(max_length = 200)

    def __unicode__(self):
        return "%s (%s)" % (self.customId, self.language.id)

# A translation of a document
class TranslatedDocument(Document):
    source = models.ForeignKey("SourceDocument")
    system = models.ForeignKey("TranslationSystem")

    def __unicode__(self):
        return "%s (%s: %s => %s)" % (self.source.customId, self.system.id,
                                      self.source.language.id, self.language.id)

# A collection of documents
class Corpus(models.Model):
    customId = models.CharField(max_length = 200)
    description = models.TextField()
    documents = models.ManyToManyField("SourceDocument", through="Document2Corpus")
    campaigns = models.ManyToManyField("EvaluationCampaign")
    language = models.ForeignKey("Language")

    def __unicode__(self):
        return "%s (%s)" % (self.customId, self.language.id)

# Intermediate table for storing the order of the documents in a corpus
# If http://pypi.python.org/pypi/django-sortedm2m is updated to django
# 1.4 we may switch to it
class Document2Corpus(models.Model):
    document = models.ForeignKey(SourceDocument)
    corpus = models.ForeignKey(Corpus)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

################################################################################
# The base class for the sentences
# Note that we do not want to work with sentences alone, instead we
# work with documents and corpora. As such information like language,
# system, etc. are stored in those classes
class Sentence(models.Model):
    text = models.TextField()
    document = models.ForeignKey(Document)

# These are the sentences in the SourceDocuments
class SourceSentence(Sentence):
    customId = models.CharField(max_length=200)

    def __unicode__(self):
        return self.customId

# Sentences produced by a translation system
class Translation(models.Model):
    sourceSentence = models.ForeignKey(SourceSentence)

    def __unicode__(self):
        return "%s - %s - %s" % (sourceSentence.__unicode__(), language.id, system.__unicode__())
