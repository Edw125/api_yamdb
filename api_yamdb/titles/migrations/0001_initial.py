# Generated by Django 2.2.16 on 2022-03-02 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Жанр произведения',
                'verbose_name_plural': 'Жанр произведения',
                'ordering': ('-title',),
            },
        ),
        migrations.CreateModel(
            name='Сategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Категория произведения',
                'verbose_name_plural': 'Категория произведения',
            },
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('year', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('description', models.TextField(verbose_name='Description')),
                ('category', models.ForeignKey(blank=True, help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='сategories', to='titles.Сategories', verbose_name='Категария')),
                ('genre', models.ManyToManyField(to='titles.Genres', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведение',
                'ordering': ('-name',),
            },
        ),
    ]
