from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('subscribe/<str:plan_key>/', views.subscribe, name='subscribe'),
    path('confirm/', views.confirm, name='confirm'),
    path('success/', views.success, name='success'),
    path('error/', views.error_page, name='error_page'),
    path('rank_skills/', views.rank_skills, name='rank_skills'), 
]
