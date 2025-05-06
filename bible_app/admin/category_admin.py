"""Admin configuration for content categories."""
from django.contrib import admin
from django.utils.html import format_html
from bible_app.models import ContentCategory, VerseCategory, Book, Chapter

class BookFilter(admin.SimpleListFilter):
    """Filtro personalizado para livros da Bíblia."""
    title = 'Livro'
    parameter_name = 'book'

    def lookups(self, request, model_admin):
        books = Book.objects.all().order_by('name')
        return [(book.id, book.name) for book in books]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(verse__chapter__book_id=self.value())
        return queryset

class ChapterFilter(admin.SimpleListFilter):
    """Filtro personalizado para capítulos."""
    title = 'Capítulo'
    parameter_name = 'chapter'

    def lookups(self, request, model_admin):
        # Só mostrar capítulos se um livro estiver selecionado
        book_id = request.GET.get('book')
        if book_id:
            chapters = Chapter.objects.filter(book_id=book_id).order_by('number')
            return [(chapter.id, f"Capítulo {chapter.number}") for chapter in chapters]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(verse__chapter_id=self.value())
        return queryset

@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    """Admin interface for ContentCategory model."""
    list_display = ['name', 'description', 'color_display', 'icon_display', 'verse_count']
    search_fields = ['name', 'description']
    list_filter = ['name']
    
    fieldsets = [
        (None, {
            'fields': ['name', 'description']
        }),
        ('Aparência', {
            'fields': ['color', 'icon'],
            'classes': ['collapse']
        }),
    ]
    
    def color_display(self, obj):
        """Exibe a cor como uma amostra visual."""
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; border-radius: 3px; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = 'Cor'
    
    def icon_display(self, obj):
        """Exibe o ícone visualmente."""
        return format_html('<i class="bi {} fs-4"></i> {}', obj.icon, obj.icon)
    icon_display.short_description = 'Ícone'
    
    def verse_count(self, obj):
        """Conta quantos versículos estão associados a esta categoria."""
        return VerseCategory.objects.filter(category=obj).count()
    verse_count.short_description = 'Versículos'

@admin.register(VerseCategory)
class VerseCategoryAdmin(admin.ModelAdmin):
    """Admin interface for VerseCategory model."""
    list_display = ['verse', 'category_with_icon', 'reference']
    list_filter = ['category', BookFilter, ChapterFilter]
    search_fields = ['verse__chapter__book__name', 'verse__chapter__number', 'verse__number', 'category__name']
    autocomplete_fields = ['verse', 'category']
    list_per_page = 20
    
    fieldsets = [
        (None, {
            'fields': ['verse', 'category']
        }),
        ('Informações Adicionais', {
            'fields': ['notes'],
            'classes': ['collapse']
        }),
    ]
    
    def reference(self, obj):
        """Exibe a referência completa do versículo."""
        verse = obj.verse
        return f"{verse.chapter.book.name} {verse.chapter.number}:{verse.number}"
    reference.short_description = 'Referência'
    
    def category_with_icon(self, obj):
        """Exibe a categoria com seu ícone e cor."""
        return format_html(
            '<span style="color: {};"><i class="bi {}"></i> {}</span>',
            obj.category.color, obj.category.icon, obj.category.name
        )
    category_with_icon.short_description = 'Categoria'
    
    class Media:
        css = {
            'all': ['https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css'],
        }
