# Generated by Django 5.0.3 on 2024-12-02 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bible_app', '0002_add_translator_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verse',
            name='translator',
            field=models.CharField(choices=[('yosef_chaim', 'Yosef Chaim'), ('netzer_netzarim', 'Netzer Netzarim')], max_length=20, verbose_name='Tradutor'),
        ),
    ]
