# Generated by Django 5.1.2 on 2024-12-07 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ('bible_app', '0007_delete_aramaicword_remove_versetag_tag_and_more'),
]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Livro')),
                ('order', models.IntegerField(default=0, verbose_name='Ordem')),
            ],
            options={
                'verbose_name': 'Livro',
                'verbose_name_plural': 'Livros',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TraducaoEspecifica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termo_original', models.CharField(max_length=100, unique=True, verbose_name='Termo Original')),
                ('traducao', models.CharField(max_length=100, verbose_name='Tradução')),
                ('notas', models.TextField(blank=True, null=True, verbose_name='Notas')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Tradução Específica',
                'verbose_name_plural': 'Traduções Específicas',
                'ordering': ['termo_original'],
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Número do Capítulo')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='bible_app.book')),
            ],
            options={
                'verbose_name': 'Capítulo',
                'verbose_name_plural': 'Capítulos',
                'ordering': ['number'],
                'unique_together': {('book', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Número do Versículo')),
                ('aramaic_text', models.TextField(verbose_name='Texto em Aramaico')),
                ('portuguese_text', models.TextField(verbose_name='Texto em Português')),
                ('translator_note', models.TextField(blank=True, null=True, verbose_name='Nota do Tradutor')),
                ('translator', models.CharField(choices=[('yosef_chaim', 'Yosef Chaim'), ('netzer_netzarim', 'Netzer Netzarim')], max_length=20, verbose_name='Tradutor')),
                ('aramaic_source', models.CharField(choices=[('curetonian', 'Antigos Evangelhos Curetonianos Siríacos'), ('sinaiticus', 'Palimpsesto Sinaítico Siríaco Antigo'), ('peshitta', 'Peshitta')], max_length=20, verbose_name='Fonte do Texto Aramaico')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verses', to='bible_app.chapter')),
            ],
            options={
                'verbose_name': 'Versículo',
                'verbose_name_plural': 'Versículos',
                'ordering': ['number'],
                'unique_together': {('chapter', 'number')},
            },
        ),
    ]