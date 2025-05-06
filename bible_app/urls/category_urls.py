from django.urls import path
from bible_app.views.category_views import category_list, category_detail

app_name = 'categories'

urlpatterns = [
    path('', category_list, name='list'),
    path('<int:category_id>/', category_detail, name='detail'),
]