# Generated by Django 2.2.16 on 2022-03-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_auto_20220302_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
