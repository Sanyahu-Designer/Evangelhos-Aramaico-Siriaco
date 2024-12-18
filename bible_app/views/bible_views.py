"""Views for main Bible navigation."""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from ..services.bible_service import BibleService
from ..services.chapter_service import ChapterService
from ..services.preferences_service import PreferencesService

def home(request):
    """Handle the home page view with Bible navigation."""
    bible_service = BibleService()
    chapter_service = ChapterService()
    preferences_service = PreferencesService()
        
    books = bible_service.get_books()
    selected_book_id = request.GET.get('book')
    selected_chapter_id = request.GET.get('chapter')
        
    user_preferences = {}
    if request.user.is_authenticated:
        try:
            user_preferences = preferences_service.get_user_preferences(request.user.id)
        except Exception as e:
            print(f"Error getting user preferences: {e}")
        
    context = {
        'books': books,
        'selected_book_id': selected_book_id,
        'user_preferences': user_preferences,
    }
        
    if selected_book_id and selected_chapter_id:
        try:
            chapter_context = bible_service.get_chapter_context(int(selected_chapter_id))
            context.update(chapter_context)
        except (ValueError, TypeError):
            # Handle invalid chapter_id
            context['verses'] = []
            context['previous_chapter'] = None
            context['next_chapter'] = None
        except Exception as e:
            # Handle other exceptions
            context['verses'] = []
            context['previous_chapter'] = None
            context['next_chapter'] = None
            print(f"Error in get_chapter_context: {e}")
        
    try:
        return render(request, 'bible_app/home.html', context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return HttpResponse("Error rendering template", status=500)

def get_chapters(request):
    """API endpoint to get chapters for a specific book."""
    book_id = request.GET.get('book_id')
    if book_id:
        chapters = BibleService.get_chapters(book_id)
        return JsonResponse(list(chapters), safe=False)
    return JsonResponse({'error': 'Book ID is required'}, status=400)