"""Content category models for Bible app."""
from django.db import models
from .verse import Verse

class ContentCategory(models.Model):
    """Categorias de conteúdo bíblico como parábolas, discursos, milagres, etc."""
    name = models.CharField('Nome da Categoria', max_length=100)
    description = models.TextField('Descrição', blank=True, null=True)
    color = models.CharField('Cor (Hexadecimal)', max_length=7, default='#3498db', 
                           help_text='Cor para destacar esta categoria, ex: #3498db')
    icon = models.CharField('Ícone', max_length=50, default='bi-bookmark', 
                          help_text='Nome do ícone Bootstrap, ex: bi-bookmark')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria de Conteúdo'
        verbose_name_plural = 'Categorias de Conteúdo'
    
    def __str__(self):
        return self.name


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
