import corpus.models
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    model = corpus.models.HumanSentence
    fields = ('customId', 'text'),
    extra = 0

class DocumentAdmin(admin.ModelAdmin):
    model = corpus.models.Document
    #fields = ('id', 'sourceLanguage'),
    inlines = [SentenceInline]
    classes = ['collapse']

admin.site.register(corpus.models.Language)
admin.site.register(corpus.models.Document, DocumentAdmin)
admin.site.register(corpus.models.Corpus)
admin.site.register(corpus.models.EvaluationCampaign)
#admin.site.register(Sentence)
