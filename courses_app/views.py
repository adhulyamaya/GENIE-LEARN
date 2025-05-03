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

# def recommend_courses(request):
#     try:
#         user_id = request.session.get("user_id")
#         if not user_id:
#             return JsonResponse({"error": "User not logged in."}, status=400)
#         user = User.objects.get(id=user_id)
#         if not user:
#             return JsonResponse({"error": "User not found."}, status=404)
#         user_skills = user.skills  
#         user_skills = {
#             'skills': user.skills ,
#         }


#         courses = Course.objects.filter(is_published=True)
#         print(f"Total courses fetched: {len(courses)}")

#         filtered_courses = filter_courses(user_skills, courses)
#         print(f"Filtered jobs count: {len(filtered_courses)}")
#         api_key = "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"

#         ranked_courses = []
        
#         if filtered_courses:
#             for course in filtered_courses:
#                 print(f"Ranking job: {course.title}")
#                 score = rank_course(user_skills, course, api_key)
#                 print(f"Score for job '{course.title}': {score}")
#                 ranked_courses.append({
#                     "course_id": course.id,
#                     "course_title": course.title,
#                     "score":score,
#                 })   
#             ranked_courses.sort(key=lambda x: x['score'], reverse=True)
        
#         print(f"Ranked courses sorted: {ranked_courses}")
#         return render(request, 'jobs/suggested_courses.html', {
#             'matched_jobs': ranked_courses,
#         })
#     except User.DoesNotExist:
#         print("Error: User not found")
#         return JsonResponse({'error': 'User not found'}, status=404)
    
#     except Exception as e:
#         print(f"Error in rank_courses view: {e}")
#         messages.error(request, f"An error occurred: {str(e)}")
#         return render(request, 'candidate_home.html', {'error': str(e)})
#         # return JsonResponse({'error': 'User not found'}, status=404)
    
 

# def recommend_courses(request):
#     try:
#         if not request.user.is_authenticated:
#             return JsonResponse({"error": "User not logged in."}, status=400)

#         user = request.user
#         profile = User.objects.get(email=user.email)

#         user_skills = {
#             'skills': profile.skills,
#         }

#         courses = Course.objects.filter(is_published=True)
#         print(f"Total courses fetched: {len(courses)}")

#         filtered_courses = filter_courses(user_skills, courses)
#         print(f"Filtered courses count: {len(filtered_courses)}")

#         api_key = "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"

#         ranked_courses = []

#         if filtered_courses:
#             for course in filtered_courses:
#                 print(f"Ranking course: {course.title}")
#                 score = rank_course(user_skills, course, api_key)
#                 print(f"Score for course '{course.title}': {score}")
#                 ranked_courses.append({
#                     "course_id": course.id,
#                     "course_title": course.title,
#                     "score": score,
#                 })
#             ranked_courses.sort(key=lambda x: x['score'], reverse=True)

#         print(f"Ranked courses sorted: {ranked_courses}")
#         return render(request, 'jobs/suggested_courses.html', {
#             'matched_jobs': ranked_courses,
#         })

#     except User.DoesNotExist:
#         print("Error: User not found")
#         return JsonResponse({'error': 'User not found'}, status=404)

#     except Exception as e:
#         print(f"Error in recommend_courses view: {e}")
#         messages.error(request, f"An error occurred: {str(e)}")
#         return render(request, 'candidate_home.html', {'error': str(e)})


def recommend_courses(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not logged in."}, status=400)

        user = request.user
        profile = User.objects.get(email=user.email)
        print(f"User profile: {profile}")

        user_skills = {
            'skills': profile.skills,
        }
        print(user_skills,".................................................................")
        print(f" data extracted: {user_skills}")

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
                })
            ranked_courses.sort(key=lambda x: x['score'], reverse=True)

        print(f"Ranked courses sorted: {ranked_courses}")
        return JsonResponse({'recommended_courses': ranked_courses}, status=200)

    except User.DoesNotExist:
        print("Error: User not found")
        return JsonResponse({'error': 'User not found'}, status=404)

    except Exception as e:
        print(f"Error in recommend_courses view: {e}")
        return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
