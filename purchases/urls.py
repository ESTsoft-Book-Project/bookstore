from django.urls import path
from . import views
app_name = 'purchases'

urlpatterns = [
    path('stripe_start/', views.stripe_start, name="stripe_start"),
    path('stripe_success/', views.stripe_success, name='stripe_success'),
    path('stripe_stopped/', views.stripe_stopped, name='stripe_stopped'),
    path('orders/', views.purchase_order_view, name='orders'),
    path('kakaopay_start/', views.kakaopay_start, name='kakaopay_start'),
    path('kakaopay_success/', views.kakaopay_success, name='kakaopay_success'),
    path('kakaopay_stopped/', views.kakaopay_stopped, name='kakaopay_stopped'),
    path('cancel/<int:purchase_id>/', views.purchase_cancel, name='order-cancle'),
]
