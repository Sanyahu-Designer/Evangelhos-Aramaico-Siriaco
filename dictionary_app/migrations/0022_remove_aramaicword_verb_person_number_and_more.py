# Generated by Django 5.1.2 on 2025-05-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0021_alter_aramaicword_options_aramaicword_dialect_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aramaicword',
            name='verb_person_number',
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='verb_person',
            field=models.CharField(blank=True, choices=[('1S', '1ª Pessoa Singular'), ('2S', '2ª Pessoa Singular'), ('3S', '3ª Pessoa Singular'), ('1P', '1ª Pessoa Plural'), ('2P', '2ª Pessoa Plural'), ('3P', '3ª Pessoa Plural')], max_length=2, null=True, verbose_name='Pessoa'),
        ),
    ]
