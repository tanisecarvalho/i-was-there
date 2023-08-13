from django.contrib import admin
from .models import Concert, Band, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):

    list_display = ('concert', 'user', 'created_on')
    search_fields = ['sentence']
    summernote_fields = ('sentence')


@admin.register(Concert)
class ConcertAdmin(SummernoteModelAdmin):

    list_display = ('band', 'date', 'user', 'slug')
    search_fields = ['country', 'city', 'date']
    prepopulated_fields = {'slug': ('date', 'country', 'band', )}


@admin.register(Band)
class BandAdmin(SummernoteModelAdmin):
    list_display = ('name', 'user', 'created_on')
    search_fields = ['name']