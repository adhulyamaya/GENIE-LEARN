from django.urls import path
from . import views

app_name = 'mentor'  

urlpatterns = [
    path('create-course/', views.create_course, name='create-course'),  
    path('dashboard/', views.mentor_dashboard, name='m_dashboard'),
    path('mentees/', views.handle_mentees, name='handle_mentees'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('chat/<int:course_id>/', views.chat_with_mentor, name='chat')

    
    

    # path('c_messages/<int:course_id>/', views.message_view, name='c_messages'),
]

