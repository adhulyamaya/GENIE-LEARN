from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.payment, name='payment'),
    path('upi_payment/', views.upi_payment, name='upi_payment'),
    path('card_payment/', views.card_payment, name='card_payment'),
    path('error/', views.error_page, name='error_page'),
    path('success/', views.success, name='success'),

]
