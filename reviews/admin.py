from django.contrib import admin

from api_yamdb.settings import VALUE_DISPLAY
from reviews.models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'title',
        'text', 'score', 'pub_date',
    )
    search_fields = ('author', 'title', 'text',)
    list_filter = ('author',)
    list_editable = (
        'author', 'title', 'text', 'score',
    )
    empty_value_display = VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    search_fields = ('author', 'text', 'pub_date',)
    list_filter = ('author',)
    list_editable = ('author', 'review', 'text',)
    empty_value_display = VALUE_DISPLAY
