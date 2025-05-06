"""Admin configuration for the Bible app."""
from django.contrib import admin
from ..models import Book, Chapter, Verse, TraducaoEspecifica, ContentCategory, VerseCategory
from bible_app.admin.book_admin import BookAdmin
from bible_app.admin.chapter_admin import ChapterAdmin
from bible_app.admin.verse_admin import VerseAdmin
from bible_app.admin.traducao_admin import TraducaoEspecificaAdmin
# Importar explicitamente o módulo category_admin para garantir que os registros sejam carregados
from bible_app.admin.category_admin import ContentCategoryAdmin, VerseCategoryAdmin

# Os novos modelos ContentCategory e VerseCategory são registrados diretamente
# em seu próprio arquivo category_admin.py usando o decorador @admin.register

# Register models with their custom admin classes
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(TraducaoEspecifica, TraducaoEspecificaAdmin)