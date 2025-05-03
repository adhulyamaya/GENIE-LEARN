import os
import glob
from django.conf import settings
from django.shortcuts import render
from .models import Course
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from user_app.models import User
from .utils import call_grouq_api
from django.http import JsonResponse
from rest_framework.response import Response
import logging

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


def build_course_recommendation_prompt(user_skills, courses):
    prompt = f"User Skills: {', '.join(user_skills)}\n\nCourses:\n"
    for course in courses:
        course_skills = course.get_skills()
        prompt += (
            f"Course Title: {course.title}\n"
            f"Skills: {', '.join(course_skills)}\n"
            f"Description: {course.description[:100]}...\n\n"
        )
    prompt += (
        "Based on the user's skills, recommend and rank the most suitable courses. "
        "List them with short reasons."
    )
    print("[DEBUG] Generated Prompt:\n", prompt)
    return prompt


def recommend_courses(request):
    try:
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"error": "User not logged in."}, status=400)
        user = User.objects.get(id=user_id)
        if not user:
            return JsonResponse({"error": "User not found."}, status=404)
        user_skills = user.skills  
        if isinstance(user_skills, str):
            user_skills = [skill.strip().lower() for skill in user_skills.split(',')] 
        logger.debug(f"[DEBUG] User Skills: {user_skills}")

        courses = Course.objects.filter(is_published=True)
        logger.debug(f"[DEBUG] Fetched {courses.count()} published courses")
        prompt = build_course_recommendation_prompt(user_skills, courses)
        recommendation = call_grouq_api(prompt)
        logger.debug("[DEBUG] GrouQ Response:", recommendation)

        return Response({
            "recommendation_raw": recommendation
        })

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found.")
        return JsonResponse({"error": "User not found."}, status=404)
    
    except Exception as e:
        logger.error(f"Error occurred while recommending courses: {str(e)}")
        return JsonResponse({"error": "An error occurred while processing the request."}, status=500)
