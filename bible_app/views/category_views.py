"""Views for content categories."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from bible_app.models import ContentCategory, VerseCategory

def category_list(request):
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

def category_detail(request, category_id):
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
    
    # Construir a URL base a partir do domínio atual
    protocol = 'https' if request.is_secure() else 'http'
    domain = request.get_host()
    categories_url = f"{protocol}://{domain}/categories/"
        
    context = {
        'category': category,
        'page_obj': page_obj,
        'verse_count': verse_categories.count(),
        'title': f'Categoria: {category.name}',
        'categories_url': categories_url
    }
    
    # Usar o template fixo que funciona em todos os ambientes
    return render(request, 'bible_app/category_detail_fixed.html', context)