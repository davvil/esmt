from django.db import models

class EvaluationCampaign(models.Model):
    id = models.CharField(primary_key = True, max_length = 200)
    description = models.TextField()

    def __unicode__(self):
        return self.id

class Language(models.Model):
    id = models.CharField(primary_key = True, max_length = 2)
    humanReadable = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.humanReadable

class Corpus(models.Model):
    id = models.CharField(primary_key = True, max_length = 200)
    description = models.TextField()
    documents = models.ManyToManyField("Document", through="Document2Corpus")
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return self.id

class Document(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    sourceLanguage = models.ForeignKey(Language)
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return self.id

# Intermediate table for storing the order of the documents in a corpus
# If http://pypi.python.org/pypi/django-sortedm2m is updated to django
# 1.4 we may switch to it
class Document2Corpus(models.Model):
    document = models.ForeignKey(Document)
    corpus = models.ForeignKey(Corpus)
    order = models.IntegerField()

class Sentence(models.Model):
    text = models.TextField()
    document = models.ForeignKey(Document)

class HumanSentence(Sentence):
    customId = models.CharField(max_length=200)

    def __unicode__(self):
        return self.customId

class TranslationSystem(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    def __unicode__(self):
        return self.id

class Translation(models.Model):
    sourceSentence = models.ForeignKey(HumanSentence)
    language = models.ForeignKey(Language)
    system = models.ForeignKey(TranslationSystem)
    text = models.TextField()
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return "%s - %s - %s" % (sourceSentence.__unicode__(), language.id, system.__unicode__())

