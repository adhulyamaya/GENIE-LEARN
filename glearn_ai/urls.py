from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'), 
    path('home/', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('user_app/', include('user_app.urls')),

]