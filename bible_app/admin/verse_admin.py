"""Admin configuration for Verse model."""
from django.contrib import admin
from django.utils.html import format_html
from ..models import Verse, VerseCategory, ContentCategory

class VerseCategoryInline(admin.TabularInline):
    model = VerseCategory
    extra = 1
    autocomplete_fields = ['category']
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"
    fields = ('category', 'notes')
    # Removendo is_primary da exibição padrão, já que não é necessário

class VerseAdmin(admin.ModelAdmin):
    list_display = ('reference', 'aramaic_preview', 'portuguese_preview', 'translator', 'get_categories')
    list_filter = ('chapter__book', 'chapter', 'translator', 'versecategory__category')
    search_fields = ('aramaic_text', 'portuguese_text', 'translator_note')
    ordering = ('chapter__book__order', 'chapter__number', 'number')
    inlines = [VerseCategoryInline]
    
    def reference(self, obj):
        return f'{obj.chapter.book.name} {obj.chapter.number}:{obj.number}'
    reference.short_description = 'Referência'
    
    def aramaic_preview(self, obj):
        return format_html('<div dir="rtl" style="font-family: \'SBL Hebrew\', serif;">{}</div>',
                         obj.aramaic_text[:100] + '...' if len(obj.aramaic_text) > 100 else obj.aramaic_text)
    aramaic_preview.short_description = 'Texto Aramaico'
    
    def portuguese_preview(self, obj):
        return obj.portuguese_text[:100] + '...' if len(obj.portuguese_text) > 100 else obj.portuguese_text
    portuguese_preview.short_description = 'Texto Português'
    
    def get_categories(self, obj):
        categories = VerseCategory.objects.filter(verse=obj).select_related('category')
        if not categories:
            return "-"
        return format_html(
            ', '.join(['<span style="color: {};"><i class="bi {}"></i> {}</span>'.format(
                cat.category.color, cat.category.icon, cat.category.name
            ) for cat in categories])
        )
    get_categories.short_description = 'Categorias'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('chapter', 'chapter__book')
        
    class Media:
        css = {
            'all': ['https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css'],
        }