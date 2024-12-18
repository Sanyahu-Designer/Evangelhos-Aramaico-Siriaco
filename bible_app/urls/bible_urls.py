"""URLs for main Bible navigation."""
from django.urls import path
from ..views.bible_views import home, get_chapters
from ..views.theme_views import update_theme

urlpatterns = [
    path('', home, name='home'),
    path('get-chapters/', get_chapters, name='get_chapters'),
    path('update-theme/', update_theme, name='update_theme'),
]