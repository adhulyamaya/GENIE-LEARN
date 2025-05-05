import os
import glob
from django.conf import settings
from django.shortcuts import render
from .models import Course
from .models import Course
from user_app.models import User
from django.http import JsonResponse
from rest_framework.response import Response
import logging
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .utils import   filter_courses, rank_course
from .models import Lesson, Enrollment
from courses_app.models import Quiz
from django.shortcuts import render, get_object_or_404
from .models import Lesson, Quiz, Question, QuizResult
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def courses(request):
    courses = Course.objects.all()
    course_data = []

    for course in courses:
        thumbnails_dir = os.path.join(settings.BASE_DIR, 'static', 'course_thumbnails')
        pattern = os.path.join(thumbnails_dir, f"course_{course.id}.*")
        matching_files = glob.glob(pattern)

        if matching_files:
            thumbnail_file = os.path.basename(matching_files[0])  
            thumbnail_path = f"course_thumbnails/{thumbnail_file}"
        else:
            thumbnail_path = f"1.jpeg" 

        course_data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "skills": course.skills,
            "author": course.author.email,
            "thumbnail": thumbnail_path,
            "difficulty": course.get_difficulty_display(),
            "category": course.category,
            "tags": course.tags,
            "subscription": course.subscription,
            "is_published": course.is_published,
            "created_at": course.created_at,
        })

    return render(request, "courses.html", {"courses": course_data})

def recommend_courses(request):
    try:
        if not request.user.is_authenticated:
            return redirect('user_app:login')  

        user = request.user
        profile = User.objects.get(email=user.email)
        print(f"User profile: {profile}")

        user_skills = {
            'skills': profile.skills,
        }
        print(user_skills, "...................")
        print(f"Data extracted: {user_skills}")

        courses = Course.objects.filter(is_published=True)
        print(f"Total courses fetched: {len(courses)}")

        filtered_courses = filter_courses(user_skills, courses)
        print(f"Filtered courses count: {len(filtered_courses)}")

        api_key = "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"

        ranked_courses = []

        if filtered_courses:
            for course in filtered_courses:
                print(f"Ranking course: {course.title}")
                score = rank_course(user_skills, course, api_key)
                print(f"Score for course '{course.title}': {score}")
                ranked_courses.append({
                    "course_id": course.id,
                    "course_title": course.title,
                    "score": score,
                    "description": course.description,
                    "skills": course.skills,
                    "author": course.author.email,
                    
                })
            ranked_courses.sort(key=lambda x: x['score'], reverse=True)

        print(f"Ranked courses sorted: {ranked_courses}")

        return render(request, 'aisuggestions.html', {'recommended_courses': ranked_courses})

    except User.DoesNotExist:
        print("Error: User not found")
        return redirect('user_app:login')

    except Exception as e:
        print(f"Error in recommend_courses view: {e}")
        return render(request, 'aisuggestions.html', {'error': f"An error occurred: {str(e)}"})


def course_detail(request, course_id):
    user=request.user
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    print(f"Enrollment found: {enrollment}")
    # print(enrollment.score)

    context = {
        'course': course,
        'enrollment': enrollment
    }
    return render(request, "course_detail.html", context)


def completed_lesson(request):
    user = request.user
    print(f"User: {user.full_name}")   

    enrollments = Enrollment.objects.filter(user=user)
    print(f"Found {len(enrollments)} enrollments for the user.") 

    enrollments = enrollments.prefetch_related('completed_lessons')
    completed_lessons = set()  
    print(f"Initial completed lessons set: {completed_lessons}")  

    for enrollment in enrollments:
        print(f"Processing enrollment for course: {enrollment.course.name}") 
        for lesson in enrollment.completed_lessons.all():
            print(f"Adding lesson: {lesson.title}") 
            completed_lessons.add(lesson)  

    print(f"Completed lessons count after processing: {len(completed_lessons)}") 

    return render(request, "completed_lessons.html", {
        "completed_lessons": list(completed_lessons)
    })



def enroll_in_course(request, lesson_id):
    print(f"Enroll request received for lesson_id: {lesson_id}")

    lesson = get_object_or_404(Lesson, id=lesson_id)
    print(f"Lesson found: {lesson.title} (Order: {lesson.order})")

    course = lesson.course
    user = request.user
    print(f"User: {user.full_name}, Course: {course.title}")

    if not user.is_authenticated:
        messages.error(request, "You must be logged in to enroll in a course.")
        return redirect('login')  

    enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
    print(f"Enrollment {'created' if created else 'retrieved'} for user: {user.full_name}")

    previous_lessons = Lesson.objects.filter(course=course, order__lt=lesson.order)
    incomplete = [l for l in previous_lessons if l not in enrollment.completed_lessons.all()]

    print(f"Previous lessons count: {previous_lessons.count()}")
    print(f"Incomplete previous lessons: {[l.title for l in incomplete]}")

    if incomplete:
        messages.error(request, "Please complete the previous lessons first.")
        print("Redirecting due to incomplete lessons.")
        return redirect('courses_app:course_detail', course_id=course.id)

    if lesson not in enrollment.completed_lessons.all():
        enrollment.completed_lessons.add(lesson)
        # enrollment.score += 10  
        enrollment.update_progress() 
        enrollment.save()

        print(f"Lesson '{lesson.title}' marked as completed.")
        print(f"Score increased by 10. Total score: {enrollment.score}")
        messages.success(request, f"Lesson '{lesson.title}' marked as completed. Progress updated. 10 points added!")
    else:
        print(f"Lesson '{lesson.title}' was already marked as completed. No score added.")
        messages.info(request, f"Lesson '{lesson.title}' was already completed. No additional score added.")

    print("Redirecting back to course detail page.")
    return redirect('courses_app:course_detail', course_id=course.id)


# courses_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Lesson, Quiz

def quiz_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz = get_object_or_404(Quiz, lesson=lesson)
    questions = quiz.questions.all()

    return render(request, 'quiz.html', {
        'lesson': lesson,
        'quiz': quiz,
        'questions': questions,
    })



def submit_quiz(request, lesson_id, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        # # Check for duplicate submission
        # if QuizResult.objects.filter(user=request.user, quiz=quiz).exists():
        #     return JsonResponse({
        #         'error': 'You have already submitted this quiz.'
        #     }, status=400)

        questions = quiz.questions.all()
        score = 0
        total = questions.count()

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                score += 1

        # Save the result to the database
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total
        )

        return JsonResponse({
            'score': score,
            'total': total,
            'course_id': quiz.lesson.course.id,
            'message': 'Quiz submitted successfully.'
        })



def get_course_progress(request, course_id):
    """Get the progress of a specific course for the logged-in user."""
    user = request.user
    enrollment = Enrollment.objects.filter(user=user, course_id=course_id).first()

    if enrollment:
        progress = enrollment.progress
        completed_lessons = enrollment.completed_lessons.count()
        total_lessons = enrollment.course.lessons.count()
        return JsonResponse({
            "progress": progress,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
        })
    else:
        return JsonResponse({"error": "Enrollment not found."}, status=404)
