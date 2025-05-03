from django.urls import path
from .import views


app_name = 'ai_suggestions'  

urlpatterns = [
    path('rank_skills/', views.rank_skills, name='rank_skills'),]
