from django.urls import path
from .views import cart_add, cart_list, cart_update, cart_delete, product_list

app_name = 'carts'

urlpatterns = [
    path('', cart_list, name='cart_list'),
    path('product/', product_list, name='product_list'),
    path('add/', cart_add, name='cart_add'),
    path('update/', cart_update, name='cart_update'),
    path('delete/', cart_delete, name='cart_delete'),
]