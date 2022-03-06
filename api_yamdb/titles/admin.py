from django.contrib import admin

from titles.models import Titles, Genres, Categories


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'rating',
        'description', 'category',
    )
    search_fields = ('name', 'year', 'rating')
    list_filter = ('name',)
    list_editable = (
        'name', 'year', 'rating',
        'description', 'category',
    )
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description',)
    search_fields = ('name', 'slug', 'description',)
    list_filter = ('name',)
    list_editable = ('name', 'slug', 'description',)
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'description',)
    search_fields = ('name', 'slug', 'description',)
    list_filter = ('name',)
    list_editable = ('name', 'slug', 'description',)
    empty_value_display = '-пусто-'
