from django.urls import path
from . import views

app_name = 'mentor_app'  

urlpatterns = [
    path('create-course/', views.create_course, name='create-course'),  
    path('dashboard/', views.mentor_dashboard, name='m_dashboard'),
    path('mentees/', views.handle_mentees, name='handle_mentees'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('messages/', views.message_view, name='message'),

    # path('messages/<int:course_id>/chat/<int:receiver_id>/', views.messages, name='messages'),
]

