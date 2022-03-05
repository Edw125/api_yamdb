from django.contrib import admin

from reviews.models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title',
                    'text', 'score',
                    'created', 
                    )
    search_fields = ('author', 'title', 'text')
    list_filter = ('author',)
    list_editable = ('author', 'title',
                    'text', 'score', 
                    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'created',)
    search_fields = ('author', 'text', 'created')
    list_filter = ('author',)
    list_editable = ('author', 'review', 'text',)
    empty_value_display = '-пусто-'
