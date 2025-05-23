# Generated by Django 5.1.2 on 2025-05-05 08:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0020_alter_grammaticalcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aramaicword',
            options={'ordering': ['aramaic_word'], 'verbose_name': 'Palavra Aramaica/Siríaca', 'verbose_name_plural': 'Palavras Aramaicas/Siríacas'},
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='dialect',
            field=models.CharField(blank=True, choices=[('CLASSIC', 'Siríaco Clássico'), ('TUROYO', 'Turoyo'), ('SURETH', 'Sureth'), ('OTHER', 'Outro')], max_length=10, null=True, verbose_name='Dialeto'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='register',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Registro'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='significado',
            field=models.TextField(blank=True, null=True, verbose_name='Significado'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='state',
            field=models.CharField(blank=True, choices=[('ABS', 'Absoluto'), ('CONS', 'Construto'), ('EMPH', 'Enfático')], max_length=4, null=True, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='variations',
            field=models.TextField(blank=True, null=True, verbose_name='Variações'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='verb_pattern',
            field=models.CharField(blank=True, choices=[('PEAL', 'Peal'), ('ETHPEEL', 'Ethpeel'), ('PAEL', 'Pael'), ('ETHPAAL', 'Ethpaal'), ('APHEL', 'Aphel'), ('ETTAPHAL', 'Ettaphal'), ('SHAPHEL', 'Shaphel'), ('ESHTAPHAL', 'Eshtaphal')], max_length=10, null=True, verbose_name='Padrão Verbal (Binyan)'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='verb_person_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Pessoa/Número Verbal'),
        ),
        migrations.AddField(
            model_name='aramaicword',
            name='verb_tense',
            field=models.CharField(blank=True, choices=[('PERF', 'Perfecto'), ('IMPERF', 'Imperfecto'), ('IMP', 'Imperativo'), ('PART', 'Particípio')], max_length=7, null=True, verbose_name='Tempo Verbal'),
        ),
        migrations.AlterField(
            model_name='aramaicword',
            name='aramaic_word',
            field=models.CharField(max_length=100, verbose_name='Palavra em Aramaico/Siríaco'),
        ),
        migrations.CreateModel(
            name='WordExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aramaic_text', models.TextField(verbose_name='Texto em Aramaico/Siríaco')),
                ('transliteration', models.TextField(verbose_name='Transliteração')),
                ('translation', models.TextField(verbose_name='Tradução')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Referência')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Criação')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='dictionary_app.aramaicword', verbose_name='Palavra')),
            ],
            options={
                'verbose_name': 'Exemplo Frasal',
                'verbose_name_plural': 'Exemplos Frasais',
                'ordering': ['word', 'created_at'],
            },
        ),
    ]
