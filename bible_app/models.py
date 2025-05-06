from django.db import models
from django.contrib.auth.models import User

__all__ = ['Book', 'Chapter', 'Verse', 'ContentCategory', 'VerseCategory', 'TraducaoEspecifica']

class Book(models.Model):
    name = models.CharField('Nome do Livro', max_length=100)
    order = models.IntegerField('Ordem', default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.IntegerField('Número do Capítulo')
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Capítulo'
        verbose_name_plural = 'Capítulos'
        unique_together = ['book', 'number']
    
    def __str__(self):
        return f"{self.book.name} - Capítulo {self.number}"

class ContentCategory(models.Model):
    """Categorias de conteúdo bíblico como parábolas, discursos, milagres, etc."""
    name = models.CharField('Nome da Categoria', max_length=100)
    description = models.TextField('Descrição', blank=True, null=True)
    color = models.CharField('Cor (Hexadecimal)', max_length=7, default='#3498db', help_text='Cor para destacar esta categoria, ex: #3498db')
    icon = models.CharField('Ícone', max_length=50, default='bi-bookmark', help_text='Nome do ícone Bootstrap, ex: bi-bookmark')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria de Conteúdo'
        verbose_name_plural = 'Categorias de Conteúdo'
    
    def __str__(self):
        return self.name

class Verse(models.Model):
    TRANSLATOR_CHOICES = [
        ('yosef_chaim', 'Yosef Chaim'),
        ('netzer_netzarim', 'Netzer Netzarim'),
    ]

    ARAMAIC_SOURCE_CHOICES = [
        ('curetonian', 'Antigos Evangelhos Curetonianos Siríacos'),
        ('sinaiticus', 'Palimpsesto Sinaítico Siríaco Antigo'),
        ('peshitta', 'Peshitta'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    number = models.IntegerField('Número do Versículo')
    aramaic_text = models.TextField('Texto em Aramaico')
    portuguese_text = models.TextField('Texto em Português')
    translator_note = models.TextField('Nota do Tradutor', blank=True, null=True)
    translator = models.CharField('Tradutor', max_length=20, choices=TRANSLATOR_CHOICES)
    aramaic_source = models.CharField('Fonte do Texto Aramaico', max_length=20, choices=ARAMAIC_SOURCE_CHOICES)
    categories = models.ManyToManyField(ContentCategory, through='VerseCategory', related_name='verses', blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        ordering = ['number']
        verbose_name = 'Versículo'
        verbose_name_plural = 'Versículos'
        unique_together = ['chapter', 'number']
    
    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.number}"
        

class VerseCategory(models.Model):
    """Associação entre versículos e categorias, com campos adicionais"""
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE)
    is_primary = models.BooleanField('É categoria principal', default=False, 
                                    help_text='Indica se esta é a categoria principal do versículo')
    notes = models.TextField('Notas', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Categorização de Versículo'
        verbose_name_plural = 'Categorizações de Versículos'
        unique_together = ['verse', 'category']
    
    def __str__(self):
        return f"{self.verse} - {self.category.name}"