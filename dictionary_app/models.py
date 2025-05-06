from django.db import models
from django.contrib.auth.models import User
from bible_app.models import Verse
from django.utils import timezone

class GrammaticalCategory(models.Model):
    name = models.CharField('Nome', max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria Gramatical'
        verbose_name_plural = 'Categorias Gramaticais'
        ordering = ['name']

class AramaicWord(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Neutro'),
    ]
    
    NUMBER_CHOICES = [
        ('S', 'Singular'),
        ('P', 'Plural'),
        ('D', 'Dual'),
    ]
    
    STATE_CHOICES = [
        ('ABS', 'Absoluto'),
        ('CONS', 'Construto'),
        ('EMPH', 'Enfático'),
    ]
    
    VERB_PATTERN_CHOICES = [
        ('PEAL', 'Pᵊʕal (Peal)'),
        ('PAEL', 'Paʕel (Pael)'),
        ('APHEL', 'ʔAp̄ʕel (Aphel)'),
        ('ETHPEEL', 'ʔEṯpᵊʕel (Ethpeel)'),
        ('ETHPAAL', 'ʔEṯpaʕal (Ethpaal)'),
        ('ETTAPHAL', 'ʔEttap̄ʕal (Ettaphal)'),
    ]
    
    VERB_TENSE_CHOICES = [
        ('PERF', 'Perfeito'),
        ('IMPERF', 'Imperfeito'),
        ('IMP', 'Imperativo'),
        ('PART', 'Particípio'),
    ]
    
    VERB_PERSON_NUMBER_CHOICES = [
        ('1S', '1ª Pessoa Singular'),
        ('2S', '2ª Pessoa Singular'),
        ('3S', '3ª Pessoa Singular'),
        ('1P', '1ª Pessoa Plural'),
        ('2P', '2ª Pessoa Plural'),
        ('3P', '3ª Pessoa Plural'),
    ]
    
    DIALECT_CHOICES = [
        ('CLASSIC', 'Siríaco Clássico'),
        ('EASTERN', 'Aramaico Oriental'),
        ('WESTERN', 'Aramaico Ocidental'),
        ('IMPERIAL', 'Aramaico Imperial'),
        ('BIBLICAL', 'Aramaico Bíblico'),
        ('JEWISH_BAB', 'Aramaico Judaico-Babilônico'),
        ('JEWISH_PAL', 'Aramaico Judaico-Palestino'),
        ('SAMARITAN', 'Aramaico Samaritano'),
        ('MANDAIC', 'Mandéu'),
        ('PALMYRENE', 'Palmireno'),
        ('NABATAEAN', 'Nabateu'),
        ('TUROYO', 'Turoyo'),
        ('MLAHSO', 'Mlahso'),
        ('SURETH', 'Sureth/Neo-Aramaico Assírio'),
        ('CHALDEAN', 'Caldeu/Neo-Aramaico Caldeu'),
        ('HERTEVIN', 'Hertevin'),
        ('SENAYA', 'Senaya'),
        ('LISHANA', 'Lishana Deni'),
        ('BOHTAN', 'Bohtan'),
        ('MODERN', 'Siríaco Moderno'),
        ('GREEK', 'Grego'),
        ('HEBREW', 'Hebraico'),
        ('OTHER', 'Outro'),
    ]

    aramaic_word = models.CharField('Palavra em Aramaico/Siríaco', max_length=100, blank=True, null=True)
    transliteration = models.CharField('Transliteração', max_length=100, blank=True, null=True)
    portuguese_translation = models.CharField('Tradução em Português', max_length=200, blank=True, null=True)
    significado = models.TextField('Significado', blank=True, null=True)
    root_word = models.CharField('Raiz da Palavra', max_length=100, blank=True, null=True)
    grammatical_category = models.ForeignKey(GrammaticalCategory, verbose_name='Categoria Gramatical', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    number = models.CharField('Número', max_length=1, choices=NUMBER_CHOICES, blank=True, null=True)
    state = models.CharField('Estado', max_length=4, choices=STATE_CHOICES, blank=True, null=True)
    
    # Campos para verbos
    verb_pattern = models.CharField('Padrão Verbal (Binyan)', max_length=10, choices=VERB_PATTERN_CHOICES, blank=True, null=True)
    verb_tense = models.CharField('Tempo Verbal', max_length=7, choices=VERB_TENSE_CHOICES, blank=True, null=True)
    verb_person_number = models.CharField('Pessoa/Número', max_length=2, choices=VERB_PERSON_NUMBER_CHOICES, blank=True, null=True)
    
    # Campos de metadados
    dialect = models.CharField('Dialeto', max_length=10, choices=DIALECT_CHOICES, blank=True, null=True)
    register = models.CharField('Registro', max_length=100, blank=True, null=True)
    variations = models.TextField('Variações', blank=True, null=True)
    
    notes = models.TextField('Anotações', blank=True, null=True)
    created_at = models.DateTimeField('Data de Criação', default=timezone.now)
    updated_at = models.DateTimeField('Data de Atualização', auto_now=True)
    favorites = models.ManyToManyField(User, verbose_name='Favoritos', related_name='favorite_words', blank=True)

    def __str__(self):
        return f"{self.aramaic_word} ({self.transliteration})"

    class Meta:
        verbose_name = 'Palavra Aramaica/Siríaca'
        verbose_name_plural = 'Palavras Aramaicas/Siríacas'
        ordering = ['aramaic_word']

class WordOccurrence(models.Model):
    word = models.ForeignKey(AramaicWord, verbose_name='Palavra', on_delete=models.CASCADE, related_name='occurrences')
    verse = models.ForeignKey(Verse, verbose_name='Versículo', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)

    def __str__(self):
        return f"{self.word} em {self.verse}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        unique_together = ['word', 'verse']

class WordCrossReference(models.Model):
    word = models.ForeignKey(AramaicWord, verbose_name='Palavra', on_delete=models.CASCADE, related_name='cross_references')
    context = models.TextField('Contexto', null=True, blank=True)
    created_at = models.DateTimeField('Data de Criação', default=timezone.now)

    def __str__(self):
        return f"{self.word} - Contexto"

    class Meta:
        verbose_name = 'Referência Cruzada'
        verbose_name_plural = 'Referências Cruzadas'
        ordering = ['word']

class WordExample(models.Model):
    word = models.ForeignKey(AramaicWord, verbose_name='Palavra', on_delete=models.CASCADE, related_name='examples')
    aramaic_text = models.TextField('Texto em Aramaico/Siríaco', blank=True, null=True)
    transliteration = models.TextField('Transliteração', blank=True, null=True)
    translation = models.TextField('Tradução', blank=True, null=True)
    reference = models.CharField('Referência', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('Data de Criação', default=timezone.now)

    def __str__(self):
        return f"Exemplo de {self.word}"

    class Meta:
        verbose_name = 'Exemplo Frasal'
        verbose_name_plural = 'Exemplos Frasais'
        ordering = ['word', 'created_at']