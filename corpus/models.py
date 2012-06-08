from django.db import models

class Language(models.Model):
    id = models.CharField(primary_key = True, max_length = 2)
    humanReadable = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.humanReadable

class Document(models.Model):
    id = models.CharField(max_length = 200, primary_key = True)
    sourceLanguage = models.ForeignKey(Language)

    def __unicode__(self):
        return self.id

class Sentence(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    text = models.TextField()
    Document = models.ForeignKey(Document)

    def __unicode__(self):
        return self.id
