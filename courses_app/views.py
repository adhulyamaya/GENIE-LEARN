import os
import glob
from django.conf import settings
from django.shortcuts import render
from .models import Course

def courses(request):
    courses = Course.objects.all()
    course_data = []

    for course in courses:
        # Absolute path to the static/course_thumbnails directory
        thumbnails_dir = os.path.join(settings.BASE_DIR, 'static', 'course_thumbnails')
        # Pattern to match course_{id}.*
        pattern = os.path.join(thumbnails_dir, f"course_{course.id}.*")
        matching_files = glob.glob(pattern)

        # Get relative static path if file found
        if matching_files:
            thumbnail_file = os.path.basename(matching_files[0])  # Get just the filename
            thumbnail_path = f"course_thumbnails/{thumbnail_file}"
        else:
            thumbnail_path = f"1.jpeg"  # fallback if no file found

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
