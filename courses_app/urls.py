from django.urls import path
from . import views

app_name = 'courses_app'  


urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('recommend_courses/', views.recommend_courses, name='recommend_courses'),

]



