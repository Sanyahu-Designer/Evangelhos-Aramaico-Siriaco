# Generated by Django 5.1.6 on 2025-05-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0024_alter_aramaicword_aramaic_word_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aramaicword',
            name='verb_pattern',
            field=models.CharField(blank=True, choices=[('PEAL', 'Pᵊʕal (Peal)'), ('PAEL', 'Paʕel (Pael)'), ('APHEL', 'ʔAp̄ʕel (Aphel)'), ('ETHPEEL', 'ʔEṯpᵊʕel (Ethpeel)'), ('ETHPAAL', 'ʔEṯpaʕal (Ethpaal)'), ('ETTAPHAL', 'ʔEttap̄ʕal (Ettaphal)')], max_length=10, null=True, verbose_name='Padrão Verbal (Binyan)'),
        ),
    ]
