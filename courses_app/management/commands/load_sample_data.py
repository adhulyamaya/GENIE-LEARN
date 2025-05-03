import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses_app.models import Course


User = get_user_model()

class Command(BaseCommand):
    help = 'Load initial course data into the database'

    def handle(self, *args, **options):
        data = [
            {
                "title": "Python for Beginners",
                "description": "An introductory course to Python programming.",
                "skills": "Python, Programming, Beginner",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/python_intro.jpg",
                "difficulty": "beginner",
                "category": "Programming",
                "tags": "Python, Beginner, Coding",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Advanced Django",
                "description": "Master Django with this advanced course.",
                "skills": "Django, Web Development, Backend, Advanced",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/advanced_django.jpg",
                "difficulty": "advanced",
                "category": "Web Development",
                "tags": "Django, Web, Backend",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Data Science with Python",
                "description": "Learn how to analyze and visualize data using Python.",
                "skills": "Python, Data Science, Pandas, Numpy",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/data_science_python.jpg",
                "difficulty": "intermediate",
                "category": "Data Science",
                "tags": "Data Science, Python, Analysis",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Web Development with React",
                "description": "Build dynamic web applications using React.js.",
                "skills": "React, JavaScript, Web Development, Frontend",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/react_web_dev.jpg",
                "difficulty": "intermediate",
                "category": "Frontend Development",
                "tags": "React, JavaScript, Web Development",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Mastering SQL for Data Analysis",
                "description": "Learn how to efficiently query and analyze data with SQL.",
                "skills": "SQL, Database, Data Analysis",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/sql_analysis.jpg",
                "difficulty": "intermediate",
                "category": "Database",
                "tags": "SQL, Data Analysis, Database",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Introduction to Machine Learning",
                "description": "An introductory course to Machine Learning algorithms.",
                "skills": "Machine Learning, Python, Data Science",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/ml_intro.jpg",
                "difficulty": "beginner",
                "category": "AI & Machine Learning",
                "tags": "Machine Learning, AI, Python",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Building APIs with Django REST Framework",
                "description": "Learn to build RESTful APIs using Django REST Framework.",
                "skills": "Django, REST API, Python, Backend",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/drf_apis.jpg",
                "difficulty": "intermediate",
                "category": "Backend Development",
                "tags": "Django, APIs, Backend, Python",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Vue.js for Beginners",
                "description": "Learn to build modern web apps using Vue.js.",
                "skills": "Vue.js, JavaScript, Frontend",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/vuejs_beginners.jpg",
                "difficulty": "beginner",
                "category": "Frontend Development",
                "tags": "Vue.js, JavaScript, Frontend",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Deep Learning with TensorFlow",
                "description": "Explore deep learning concepts with TensorFlow.",
                "skills": "Deep Learning, TensorFlow, AI, Python",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/tensorflow_dl.jpg",
                "difficulty": "advanced",
                "category": "AI & Machine Learning",
                "tags": "Deep Learning, TensorFlow, Python, AI",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Agile Project Management",
                "description": "Learn the basics of Agile project management.",
                "skills": "Project Management, Agile, Scrum",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/agile_pm.jpg",
                "difficulty": "beginner",
                "category": "Management",
                "tags": "Agile, Project Management, Scrum",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Full Stack Web Development",
                "description": "Become a full-stack developer using the MERN stack.",
                "skills": "MongoDB, Express, React, Node.js, Full Stack",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/course_2.jpeg",
                "difficulty": "advanced",
                "category": "Web Development",
                "tags": "MERN, Full Stack, JavaScript",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Docker and Kubernetes for Beginners",
                "description": "Learn the basics of Docker and Kubernetes for container orchestration.",
                "skills": "Docker, Kubernetes, DevOps",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/docker_kubernetes.jpg",
                "difficulty": "intermediate",
                "category": "DevOps",
                "tags": "Docker, Kubernetes, DevOps",
                "subscription": "FREE",  # Add subscription field here
                "is_published": True
            },
            {
                "title": "Introduction to Cloud Computing",
                "description": "Understand cloud computing concepts and how to use AWS and Azure.",
                "skills": "Cloud Computing, AWS, Azure",
                "author": "admin@gmail.com",
                "thumbnail": "course_thumbnails/cloud_computing.jpg",
                "difficulty": "beginner",
                "category": "Cloud Computing",
                "tags": "Cloud, AWS, Azure",
                "subscription": "PRO",  # Add subscription field here
                "is_published": True
            }
        ]

        for course_data in data:
            try:
                user = User.objects.get(email=course_data["author"])
                course, created = Course.objects.get_or_create(
                    title=course_data["title"],
                    defaults={
                        "description": course_data["description"],
                        "skills": course_data["skills"],
                        "author": user,
                        "thumbnail": course_data["thumbnail"],
                        "difficulty": course_data["difficulty"],
                        "category": course_data["category"],
                        "tags": course_data["tags"],
                        "subscription": course_data["subscription"],  # Add subscription field here
                        "is_published": course_data["is_published"]
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added course: {course.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Course already exists: {course.title}"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Author not found: {course_data['author']}"))
