from django.contrib import admin
from .models import Concert, Band, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):

    summernote_fields = ('sentence')


admin.site.register(Concert)
admin.site.register(Band)
