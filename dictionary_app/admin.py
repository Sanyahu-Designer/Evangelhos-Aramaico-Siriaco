from django.contrib import admin
from django import forms
from django.db import connection
from .models import GrammaticalCategory, AramaicWord, WordOccurrence, WordCrossReference, WordExample

@admin.register(GrammaticalCategory)
class GrammaticalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

class WordOccurrenceInline(admin.TabularInline):
    model = WordOccurrence
    extra = 0
    readonly_fields = ['verse']
    can_delete = False
    verbose_name = 'Ocorrência'
    verbose_name_plural = 'Ocorrências'
    fields = ['verse']
    max_num = 20  # Aumentado para exibir mais ocorrências
    show_change_link = True  # Adiciona um link para editar a ocorrência
    
    def has_add_permission(self, request, obj=None):
        # Permite adição de ocorrências
        return True
        
    def get_formset(self, request, obj=None, **kwargs):
        # Este método é chamado quando o formset é criado
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            # Se estamos editando um objeto existente, vamos verificar se há ocorrências
            # Se não houver, tentamos detectá-las e salvá-las
            from .services import WordOccurrenceService
            from bible_app.models import Verse
            
            # Verifica se já existem ocorrências
            if obj.occurrences.count() == 0 and obj.aramaic_word:
                # Detecta ocorrências
                results = WordOccurrenceService.detect_word_occurrences(obj.aramaic_word)
                
                # Salva as ocorrências no banco de dados
                for occurrence in results['occurrences']:
                    try:
                        verse = Verse.objects.get(
                            chapter__book__name=occurrence['book'],
                            chapter__number=occurrence['chapter'],
                            number=occurrence['verse']
                        )
                        # Cria a ocorrência se não existir
                        WordOccurrence.objects.get_or_create(word=obj, verse=verse)
                    except Verse.DoesNotExist:
                        continue
        return formset

class WordExampleInline(admin.StackedInline):
    model = WordExample
    extra = 1
    fields = ['aramaic_text', 'transliteration', 'translation', 'reference']
    verbose_name = 'Exemplo de uso'
    verbose_name_plural = 'Exemplos de uso'

class WordCrossReferenceInline(admin.StackedInline):
    model = WordCrossReference
    extra = 1
    fields = ['context']
    verbose_name = 'Referência'
    verbose_name_plural = 'Referências'

@admin.register(AramaicWord)
class AramaicWordAdmin(admin.ModelAdmin):
    list_display = ['aramaic_word', 'transliteration', 'portuguese_translation', 'grammatical_category']
    search_fields = ['aramaic_word', 'transliteration', 'portuguese_translation']
    list_filter = ['grammatical_category', 'gender', 'state', 'verb_pattern', 'verb_tense', 'dialect']
    
    fieldsets = [
        ('Informações Básicas', {
            'fields': [
                'aramaic_word', 'transliteration', 'portuguese_translation', 'significado',
            ]
        }),
        ('Morfologia', {
            'fields': [
                'grammatical_category', 'state', 'gender', 'root_word'
            ],
            'classes': ['collapse']
        }),
        ('Informações Verbais', {
            'fields': ['verb_pattern', 'verb_tense', 'verb_person_number'],
            'classes': ['collapse']
        }),
        ('Metadados', {
            'fields': ['dialect', 'register', 'variations'],
            'classes': ['collapse']
        }),
        ('Notas', {
            'fields': ['notes'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [WordExampleInline, WordCrossReferenceInline, WordOccurrenceInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "grammatical_category":
            kwargs["widget"] = forms.Select(attrs={'class': 'select-only'})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Ao salvar a palavra, detecta automaticamente as ocorrências."""
        # Primeiro salvamos o objeto para garantir que ele exista no banco
        super().save_model(request, obj, form, change)
        
        # Se for uma nova palavra ou o texto em aramaico foi alterado
        if not change or form.changed_data and 'aramaic_word' in form.changed_data:
            from .services import WordOccurrenceService
            from bible_app.models import Verse
            from django.db import transaction
            
            try:
                with transaction.atomic():
                    # Remove todas as ocorrências antigas
                    WordOccurrence.objects.filter(word=obj).delete()
                    
                    # Detecta e salva novas ocorrências
                    results = WordOccurrenceService.detect_word_occurrences(obj.aramaic_word)
                    for occ in results['occurrences']:
                        try:
                            verse = Verse.objects.get(
                                chapter__book__name=occ['book'],
                                chapter__number=occ['chapter'],
                                number=occ['verse']
                            )
                            # Verifica se já existe uma ocorrência antes de criar
                            WordOccurrence.objects.get_or_create(
                                word=obj,
                                verse=verse
                            )
                        except Verse.DoesNotExist:
                            continue
            except Exception as e:
                # Se houver algum erro, tenta limpar todas as ocorrências
                WordOccurrence.objects.filter(word=obj).delete()
                raise e

@admin.register(WordExample)
class WordExampleAdmin(admin.ModelAdmin):
    list_display = ['word', 'transliteration', 'translation', 'reference']
    search_fields = ['word__aramaic_word', 'transliteration', 'translation', 'reference']
    list_filter = ['word__grammatical_category']
    autocomplete_fields = ['word']
