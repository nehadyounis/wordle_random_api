# Generated by Django 4.2.4 on 2023-08-08 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words_api', '0003_alter_word_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
