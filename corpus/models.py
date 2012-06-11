from django.db import models

class EvaluationCampaign(models.Model):
    id = models.CharField(primary_key = True, max_length = 200)
    description = models.TextField()

    def __unicode__(self):
        return self.id

class Corpus(models.Model):
    id = models.CharField(primary_key = True, max_length = 200)
    description = models.TextField()
    documents = models.ManyToManyField("Document")
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return self.id

class Language(models.Model):
    id = models.CharField(primary_key = True, max_length = 2)
    humanReadable = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.humanReadable

class Document(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    sourceLanguage = models.ForeignKey(Language)
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return self.id

class Sentence(models.Model):
    userId = models.CharField(max_length=200)
    text = models.TextField()
    Document = models.ForeignKey(Document)

    def __unicode__(self):
        return self.userId

class TranslationSystem(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    def __unicode__(self):
        return self.id

class Translation(models.Model):
    sourceSentence = models.ForeignKey(Sentence)
    language = models.ForeignKey(Language)
    system = models.ForeignKey(TranslationSystem)
    text = models.TextField()
    campaigns = models.ManyToManyField("EvaluationCampaign")

    def __unicode__(self):
        return "%s - %s - %s" % (sourceSentence.__unicode__(), language.id, system.__unicode__())

