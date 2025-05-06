from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from bible_app.services.bible_service import BibleService
from bible_app.services.chapter_service import ChapterService
from bible_app.services.preferences_service import PreferencesService
from bible_app.models import Chapter, Verse, ContentCategory, VerseCategory

def get_chapters(request):
    """API endpoint to get chapters for a specific book."""
    book_id = request.GET.get('book_id')
    if not book_id:
        return JsonResponse({'error': 'Book ID is required'}, status=400)
    
    bible_service = BibleService()
    try:
        chapters = bible_service.get_chapters(book_id)
        return JsonResponse(chapters, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search(request):
    """API endpoint para buscar versículos."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    bible_service = BibleService()
    results = bible_service.search_verses(query)
    return JsonResponse({'results': results})

def categories_view(request):
    """View para listar todas as categorias de conteúdo."""
    categories = ContentCategory.objects.all().order_by('name')
    
    # Contar quantos versículos cada categoria possui
    for category in categories:
        category.verse_count = VerseCategory.objects.filter(category=category).count()
    
    context = {
        'categories': categories,
        'title': 'Categorias de Conteúdo Bíblico'
    }
    
    return render(request, 'bible_app/category_list.html', context)

def category_detail_view(request, category_id):
    """View para mostrar todos os versículos de uma categoria específica."""
    category = get_object_or_404(ContentCategory, id=category_id)
    
    # Obter todos os versículos desta categoria
    verse_categories = VerseCategory.objects.filter(category=category).select_related(
        'verse', 'verse__chapter', 'verse__chapter__book'
    ).order_by('verse__chapter__book__name', 'verse__chapter__number', 'verse__number')
    
    # Paginação
    paginator = Paginator(verse_categories, 10)  # 10 versículos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'verse_count': verse_categories.count(),
        'title': f'Categoria: {category.name}'
    }
    
    return render(request, 'bible_app/category_detail.html', context)

def home(request):
    """Handle the home page view with Bible navigation."""
    bible_service = BibleService()
    chapter_service = ChapterService()
    preferences_service = PreferencesService()
    
    print("DEBUG - Request params:", request.GET)
    
    selected_book_id = request.GET.get('book')
    selected_chapter_id = request.GET.get('chapter')
    selected_verse = request.GET.get('verse')  # Versículo único
    selected_category_id = request.GET.get('category')  # Nova categoria selecionada
    
    # Novos parâmetros para destacar um intervalo de versículos
    highlight_start = request.GET.get('highlight_start')
    highlight_end = request.GET.get('highlight_end')
    
    print("DEBUG - Selected book:", selected_book_id)
    print("DEBUG - Selected chapter:", selected_chapter_id)
    print("DEBUG - Selected verse:", selected_verse)
    print("DEBUG - Selected category:", selected_category_id)
    print("DEBUG - Highlight start:", highlight_start)
    print("DEBUG - Highlight end:", highlight_end)
    
    # Obter todas as categorias de conteúdo disponíveis
    content_categories = ContentCategory.objects.all().order_by('name')
    
    context = {
        'books': bible_service.get_books(),
        'content_categories': content_categories,
        'selected_book_id': selected_book_id,
        'selected_chapter_id': selected_chapter_id,
        'selected_category_id': selected_category_id,
        'user_preferences': {},
        'verses': [],
        'previous_chapter': None,
        'next_chapter': None,
        'highlight_start': highlight_start,
        'highlight_end': highlight_end
    }
    
    if request.user.is_authenticated:
        try:
            context['user_preferences'] = preferences_service.get_user_preferences(request.user.id)
        except Exception as e:
            print(f"Error getting user preferences: {e}")
    
    if selected_book_id and selected_chapter_id:
        try:
            # Se vier da busca (tem versículo), usa o número do capítulo
            if selected_verse:
                chapter = Chapter.objects.get(
                    book_id=selected_book_id,
                    number=selected_chapter_id
                )
            else:
                # Se for navegação normal, usa o ID do capítulo
                chapter = Chapter.objects.get(
                    id=selected_chapter_id,
                    book_id=selected_book_id
                )
            
            print(f"DEBUG - Loading verses for chapter {chapter}")
            
            # Base query
            verses_query = Verse.objects.select_related('chapter', 'chapter__book')
            
            # Se tiver um intervalo de versículos para destacar, mostrar apenas os versículos do intervalo
            if highlight_start and highlight_end:
                try:
                    # Converter para inteiros
                    start_verse = int(highlight_start)
                    end_verse = int(highlight_end)
                    
                    # Filtrar apenas os versículos no intervalo especificado
                    verses_query = verses_query.filter(
                        chapter=chapter,
                        number__gte=start_verse,
                        number__lte=end_verse
                    )
                    # Todos os versículos mostrados já estão no intervalo, então todos serão destacados
                except (ValueError, TypeError):
                    # Se houver erro na conversão dos números, mostrar o capítulo inteiro
                    verses_query = verses_query.filter(chapter=chapter)
            # Se tiver um versículo específico da busca, mostrar apenas ele
            elif selected_verse:
                verses_query = verses_query.filter(
                    chapter=chapter,
                    number=selected_verse
                )
            else:
                # Caso contrário, mostrar todos os versículos do capítulo
                verses_query = verses_query.filter(
                    chapter=chapter
                )
                
            # Filtrar por categoria, se especificado
            if selected_category_id:
                try:
                    # Obter os IDs dos versículos que pertencem à categoria selecionada
                    verse_ids = VerseCategory.objects.filter(
                        category_id=int(selected_category_id)
                    ).values_list('verse_id', flat=True)
                    
                    # Filtrar os versículos pelo ID
                    verses_query = verses_query.filter(id__in=verse_ids)
                    
                    # Adicionar a categoria selecionada ao contexto
                    context['selected_category'] = ContentCategory.objects.get(id=int(selected_category_id))
                except (ValueError, TypeError, ContentCategory.DoesNotExist):
                    # Ignorar se a categoria não existir ou o ID não for válido
                    pass
            
            verses_list = list(verses_query.order_by('number'))
            print(f"DEBUG - Found {len(verses_list)} verses")
            
            if verses_list:
                print(f"DEBUG - First verse: {verses_list[0].aramaic_text[:100]}")
            
            context.update({
                'chapter': chapter,
                'verses': verses_list,
                'previous_chapter': Chapter.objects.filter(
                    book_id=selected_book_id,
                    number__lt=chapter.number
                ).order_by('-number').first(),
                'next_chapter': Chapter.objects.filter(
                    book_id=selected_book_id,
                    number__gt=chapter.number
                ).order_by('number').first()
            })
            
            print("DEBUG - Context updated with verses")
            
        except Chapter.DoesNotExist:
            print(f"Error: Chapter {selected_chapter_id} not found")
        except Exception as e:
            print(f"Error loading verses: {str(e)}")
    
    return render(request, 'bible_app/home.html', context)