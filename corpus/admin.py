import corpus.models
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    model = corpus.models.SourceSentence
    fields = ('customId', 'text'),
    extra = 0

class SourceDocumentAdmin(admin.ModelAdmin):
    model = corpus.models.SourceDocument
    #fields = ('id', 'sourceLanguage'),
    inlines = [SentenceInline]
    classes = ['collapse']

admin.site.register(corpus.models.Language)
admin.site.register(corpus.models.SourceDocument, SourceDocumentAdmin)
admin.site.register(corpus.models.Corpus)
admin.site.register(corpus.models.EvaluationCampaign)
#admin.site.register(Sentence)
