from django.urls import path
from .views import book_list, book_detail

app_name = 'book'

urlpatterns = [
    path('book/', book_list, name='book_list'),
    path('book/<slug:handle>/', book_detail, name='book_detail'),
]
