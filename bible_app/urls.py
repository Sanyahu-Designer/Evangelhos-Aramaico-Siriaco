"""Main URL configuration for the Bible app."""
from django.urls import path, include
from django.shortcuts import render
from .views.cache_monitor import cache_dashboard
from .views.bible_views import home, get_chapters, categories_view, category_detail_view
from .views.search_views import search_content

app_name = 'bible_app'

urlpatterns = [
    path('', home, name='home'),
    path('books/', include('bible_app.urls.book_urls')),
    path('verses/', include('bible_app.urls.verse_urls')),
    path('auth/', include('bible_app.urls.auth_urls')),
    path('chapters/', get_chapters, name='get_chapters'),
    path('search/', search_content, name='search'),
    path('cache-dashboard/', cache_dashboard, name='cache_dashboard'),
    # URLs para categorias de conteúdo
    path('test-category/', lambda request: render(request, 'bible_app/test_category.html'), name='test_category'),
    path('categories/', categories_view, name='category_list'),
    path('categories/<int:category_id>/', category_detail_view, name='category_detail'),
]