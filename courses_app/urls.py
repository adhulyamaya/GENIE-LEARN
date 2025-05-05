from django.urls import path
from . import views

app_name = 'courses_app'  

urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('recommend_courses/', views.recommend_courses, name='recommend_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:lesson_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('completed_lessons/', views.completed_lesson, name='completed_lessons'),
    path('lesson/<int:lesson_id>/quiz/', views.quiz_view, name='quiz'),
    path('lesson/<int:lesson_id>/quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('mentor_support/<int:course_id>/', views.mentor_support, name='mentor_support'),

]



