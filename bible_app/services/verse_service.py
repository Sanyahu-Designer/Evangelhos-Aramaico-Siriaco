"""Service for handling verse-related operations."""
from django.db.models import QuerySet
from ..models import Verse
from ..utils.query_utils import filter_by_text, paginate_queryset

class VerseService:
    @staticmethod
    def get_verses_by_chapter(chapter_id: int) -> QuerySet:
        """Retrieve verses for a specific chapter with related data.
        
        Args:
            chapter_id (int): ID of the chapter
            
        Returns:
            QuerySet: Queryset of verses with related book and chapter data
        """
        return Verse.objects.filter(
            chapter_id=chapter_id
        ).select_related('chapter', 'chapter__book')
    
    @staticmethod
    def search_verses(search_text: str, page: int = 1):
        """Search verses by text in both Aramaic and Portuguese.
        Also recognizes biblical references in the format 'Book Chapter:Verse' or 'Book Chapter:Verse-Verse'.
        
        Args:
            search_text (str): Text to search for or biblical reference
            page (int): Page number for pagination
            
        Returns:
            dict or QuerySet: For range references, returns a dict with range info and verses;
                             otherwise returns a filtered and paginated queryset of verses
        """
        import re
        
        # Verificar se a busca é uma referência bíblica em um dos formatos:
        # 1. "Livro Capítulo:Versículo" (ex: "Mateus 1:1")
        # 2. "Livro Capítulo:Versículo-Versículo" (ex: "Mateus 1:1-5")
        
        # Padrão para referência simples
        single_verse_pattern = r'^(\d*\s*[A-Za-zÀ-ÖØ-öø-ÿ]+)\s+(\d+):(\d+)$'
        # Padrão para intervalo de versículos
        verse_range_pattern = r'^(\d*\s*[A-Za-zÀ-ÖØ-öø-ÿ]+)\s+(\d+):(\d+)-(\d+)$'
        
        # Verificar primeiro se é um intervalo de versículos
        range_match = re.match(verse_range_pattern, search_text.strip())
        if range_match:
            book_name, chapter_number, start_verse, end_verse = range_match.groups()
            try:
                # Converter para inteiros
                chapter_num = int(chapter_number)
                start_verse_num = int(start_verse)
                end_verse_num = int(end_verse)
                
                # Garantir que o intervalo está na ordem correta
                if start_verse_num > end_verse_num:
                    start_verse_num, end_verse_num = end_verse_num, start_verse_num
                
                # Buscar todos os versículos no intervalo
                verses = Verse.objects.filter(
                    chapter__book__name__icontains=book_name.strip(),
                    chapter__number=chapter_num,
                    number__gte=start_verse_num,
                    number__lte=end_verse_num
                ).select_related('chapter', 'chapter__book').order_by('number')
                
                # Se encontrou versículos, retorna informações sobre o intervalo
                if verses.exists():
                    # Pegar o primeiro versículo para obter informações do livro e capítulo
                    first_verse = verses.first()
                    
                    # Retornar um dicionário com informações sobre o intervalo e os versículos
                    return {
                        'is_range': True,
                        'book_id': first_verse.chapter.book.id,
                        'book_name': first_verse.chapter.book.name,
                        'chapter_id': first_verse.chapter.id,
                        'chapter_number': first_verse.chapter.number,
                        'start_verse': start_verse_num,
                        'end_verse': end_verse_num,
                        'verses': verses
                    }
                
                # Se não encontrou nada, tenta uma busca mais flexível
                verses = Verse.objects.filter(
                    chapter__book__name__icontains=book_name.strip(),
                    chapter__number=chapter_num
                ).select_related('chapter', 'chapter__book').order_by('number')
                
                if verses.exists():
                    first_verse = verses.first()
                    return {
                        'is_range': True,
                        'book_id': first_verse.chapter.book.id,
                        'book_name': first_verse.chapter.book.name,
                        'chapter_id': first_verse.chapter.id,
                        'chapter_number': first_verse.chapter.number,
                        'start_verse': 1,  # Mostrar todo o capítulo
                        'end_verse': 999,  # Um número grande para incluir todos os versículos
                        'verses': verses
                    }
                
                # Se ainda não encontrou nada, retorna uma lista vazia
                return paginate_queryset(Verse.objects.none(), 10, page)
            except (ValueError, TypeError):
                # Se houver erro na conversão dos números, continua para verificar outros padrões
                pass
        
        # Se não for um intervalo, verifica se é um versículo único
        match = re.match(single_verse_pattern, search_text.strip())
        
        if match:
            # É uma referência bíblica para um versículo único
            book_name, chapter_number, verse_number = match.groups()
            
            try:
                # Buscar pelo livro, capítulo e versículo específicos
                verses = Verse.objects.filter(
                    chapter__book__name__icontains=book_name.strip(),
                    chapter__number=int(chapter_number),
                    number=int(verse_number)
                ).select_related('chapter', 'chapter__book')
                
                # Se não encontrou nada, tenta uma busca mais flexível
                if not verses.exists():
                    # Buscar apenas pelo nome do livro e número do capítulo
                    verses = Verse.objects.filter(
                        chapter__book__name__icontains=book_name.strip(),
                        chapter__number=int(chapter_number)
                    ).select_related('chapter', 'chapter__book').order_by('number')
            except (ValueError, TypeError):
                # Se houver erro na conversão dos números, faz busca normal
                verses = Verse.objects.select_related('chapter', 'chapter__book')
                verses = filter_by_text(verses, search_text, [
                    'aramaic_text', 'portuguese_text', 'translator_note', 'chapter__book__name'
                ])
        else:
            # Busca normal por texto
            verses = Verse.objects.select_related('chapter', 'chapter__book')
            verses = filter_by_text(
                verses, 
                search_text, 
                [
                    'aramaic_text',
                    'portuguese_text',
                    'translator_note',
                    'chapter__book__name',  # Nome do livro
                ]
            )
        
        return paginate_queryset(verses, 10, page)  # 10 resultados por página

    @staticmethod
    def create_verse(chapter, number: int, aramaic_text: str, portuguese_text: str, 
                    translator: str, translator_note: str = None) -> Verse:
        """Create a new verse.
        
        Args:
            chapter: Chapter instance
            number (int): Verse number
            aramaic_text (str): Aramaic text
            portuguese_text (str): Portuguese text
            translator (str): Translator identifier
            translator_note (str, optional): Translator's note
            
        Returns:
            Verse: Created verse instance
        """
        return Verse.objects.create(
            chapter=chapter,
            number=number,
            aramaic_text=aramaic_text,
            portuguese_text=portuguese_text,
            translator=translator,
            translator_note=translator_note
        )

    @staticmethod
    def get_next_verse_number(chapter_id: int) -> int:
        """Get the next available verse number for a chapter."""
        last_verse = Verse.objects.filter(chapter_id=chapter_id).order_by('-number').first()
        return (last_verse.number + 1) if last_verse else 1