from django.urls import path
from .views import cart_add, cart_view, cart_update, cart_delete, cart_list, checkout_view, checkout_list

app_name = 'carts'

urlpatterns = [
    path('', cart_view, name='view'),
    path('list/', cart_list, name='list'),
    path('update/', cart_update, name='update'),
    path('add/', cart_add, name='add'),
    path('delete/', cart_delete, name='delete'),
    path('checkout/view/', checkout_view, name='checkout_view'),
    path('checkout/list/', checkout_list, name='checkout_list'),
]
