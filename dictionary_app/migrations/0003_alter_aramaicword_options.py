# Generated by Django 5.1.2 on 2024-12-22 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0002_remove_aramaicword_pronunciation_audio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aramaicword',
            options={'ordering': ['aramaic_word'], 'verbose_name': 'Aramaico/Português', 'verbose_name_plural': 'Aramaico/Português'},
        ),
    ]
