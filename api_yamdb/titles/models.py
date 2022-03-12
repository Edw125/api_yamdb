from django.db import models


class Genres(models.Model):
    name = models.CharField(
        'Name', max_length=50
    )
    slug = models.SlugField(
        'Slug', unique=True
    )
    description = models.TextField(
        'Description', blank=True,
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(
        'Name', blank=True, max_length=50
    )
    slug = models.SlugField(
        'Slug', unique=True
    )
    description = models.TextField(
        'Description', blank=True, null=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведения'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Name', max_length=200
    )
    year = models.IntegerField(
        blank=True, null=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='сategories',
        blank=True, null=True,
        verbose_name='Категория',
        help_text='Выберите категорию'
    )
    rating = models.IntegerField(
        blank=True, null=True,
    )
    description = models.TextField(
        'Description', blank=True, null=True,
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='titles',
        verbose_name="Жанр"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
