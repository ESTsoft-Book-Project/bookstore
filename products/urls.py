from django.urls import path
from .views import book_list, book_detail, create_product, update_product, delete_product, create_comment, delete_comment
from . import views

app_name = 'book'

urlpatterns = [
    path('book/', book_list, name='book_list'),
    path('book/create/', create_product, name='create_product'),
    path('book/<slug:handle>/', book_detail, name='book_detail'),
    path('book/update/<slug:handle>/', update_product, name='update_product'),
    path('book/delete/<slug:handle>/', delete_product, name='delete_product'),
    path("book/<slug:handle>/comment/write/", create_comment, name='create_comment'),
    path("book/<slug:handle>/comment/delete/<int:comment_id>/", delete_comment, name='delete_comment')

]
