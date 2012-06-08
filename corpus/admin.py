from corpus.models import Language,Document,Sentence
from django.contrib import admin

class SentenceInline(admin.TabularInline):
    fields = ('id', 'text'),
    model = Sentence
    extra = 0

class DocumentAdmin(admin.ModelAdmin):
    fields = ('id', 'sourceLanguage'),
    inlines = [SentenceInline]
    classes = ['collapse']

admin.site.register(Language)
admin.site.register(Document, DocumentAdmin)
#admin.site.register(Sentence)
