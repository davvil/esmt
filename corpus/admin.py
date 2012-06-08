import corpus.models
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    model = corpus.models.Sentence
    fields = ('id', 'text'),
    extra = 0

class DocumentAdmin(admin.ModelAdmin):
    model = corpus.models.Sentence
    fields = ('id', 'sourceLanguage'),
    inlines = [SentenceInline]
    classes = ['collapse']

admin.site.register(corpus.models.Language)
admin.site.register(corpus.models.Document, DocumentAdmin)
admin.site.register(corpus.models.Corpus)
#admin.site.register(Sentence)
