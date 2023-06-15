from django.urls import path
from .views import book_list, book_detail, create_product, delete_product

app_name = 'book'

urlpatterns = [
    path('book/', book_list, name='book_list'),
    path('book/create/', create_product, name='create_product'),
    path('book/<slug:handle>/', book_detail, name='book_detail'),
    path('book/delete/<slug:handle>/', delete_product, name='delete_product'),
]
