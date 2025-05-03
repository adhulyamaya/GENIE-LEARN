from django.urls import path
from . import views

app_name = 'courses_app'  # Namespace for better URL handling


urlpatterns = [
    path('courses/', views.courses, name='courses'),
    

]



