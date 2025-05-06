from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from ..services.verse_service import VerseService
from ..services.book_service import BookService
from ..services.chapter_service import ChapterService
import re

def search_content(request):
    """
    Endpoint para busca unificada de conteúdo (livros, capítulos e versículos)
    """
    query = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)
    
    if not query:
        return JsonResponse({'results': []})

    try:
        page = int(page)
    except ValueError:
        page = 1

    # Verificar se é uma busca por intervalo de versículos
    # Padrão para intervalo de versículos: "Livro Capítulo:Versículo-Versículo"
    verse_range_pattern = r'^(\d*\s*[A-Za-zÀ-ÖØ-öø-ÿ]+)\s+(\d+):(\d+)-(\d+)$'
    range_match = re.match(verse_range_pattern, query.strip())
    
    # Busca versículos
    search_result = VerseService.search_verses(query, page)
    
    # Se o resultado é um dicionário com informações de intervalo, redireciona para a página do capítulo
    if isinstance(search_result, dict) and search_result.get('is_range'):
        # Log para debug
        print(f"DEBUG - Redirecionando para intervalo de versículos: {search_result}")
        
        # Redirecionar para a página do capítulo com destaque para os versículos
        url = f"/?book={search_result['book_id']}&chapter={search_result['chapter_number']}&highlight_start={search_result['start_verse']}&highlight_end={search_result['end_verse']}"
        
        # Usar HttpResponseRedirect com status 302 para garantir que o navegador siga o redirecionamento
        response = HttpResponseRedirect(url)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    # Caso contrário, continua com o comportamento normal
    results = []
    verses = search_result  # Agora search_result é o QuerySet de versículos
    
    for verse in verses:
        # Construir a URL usando o livro, capítulo e versículo
        url = f"/?book={verse.chapter.book.id}&chapter={verse.chapter.number}&verse={verse.number}"
        results.append({
            'type': 'verse',
            'id': verse.id,
            'title': f'{verse.chapter.book.name} {verse.chapter.number}:{verse.number}',
            'text': verse.portuguese_text[:100] + '...' if len(verse.portuguese_text) > 100 else verse.portuguese_text,
            'url': url
        })

    return JsonResponse({'results': results})
