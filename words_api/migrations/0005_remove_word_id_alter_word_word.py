# Generated by Django 4.2.4 on 2023-08-08 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words_api', '0004_alter_word_word'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='id',
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, unique=True),
        ),
    ]
