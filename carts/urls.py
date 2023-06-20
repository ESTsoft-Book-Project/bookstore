from django.urls import path
from .views import cart_add, cart_list

app_name = 'carts'

urlpatterns = [
    path('', cart_list, name='cart_list'),
    path('add/', cart_add, name='cart_add'),
]