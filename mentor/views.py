from django.shortcuts import render
from courses_app.models import Course
from user_app.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from courses_app.models import Course, ChatMessage

#create course view
# def create_course(request):
#     if request.method == 'POST':
#         course_name = request.POST.get('course_name')
#         course_description = request.POST.get('course_description')
#         course_price = request.POST.get('course_price')
#         course_duration = request.POST.get('course_duration')
#         course_level = request.POST.get('course_level')
#         new_course = Course(
#             name=course_name,
#             description=course_description,
#             price=course_price,
#             duration=course_duration,
#             level=course_level
#         )
#         new_course.save()
        
#         return render(request, 'schedule.html', {'course': new_course})
    
#     return render(request, 'm_dashboard.html')


def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        price = request.POST.get('price') or 0.00
        difficulty = request.POST.get('difficulty')
        subscription = request.POST.get('subscription')
        category = request.POST.get('category')
        tags = request.POST.get('tags')

        # Debugging print statements
        print("Received POST data:")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Skills: {skills}")
        print(f"Price: {price}")
        print(f"Difficulty: {difficulty}")
        print(f"Subscription: {subscription}")
        print(f"Category: {category}")
        print(f"Tags: {tags}")
        print(f"Author: {request.user}")

        new_course = Course(
            title=title,
            description=description,
            skills=skills,
            price=price,
            difficulty=difficulty,
            subscription=subscription,
            category=category,
            tags=tags,
            author=request.user
        )
        new_course.save()

        print("Course saved successfully:", new_course)

        return render(request, 'schedule.html', {'course': new_course})

    print("GET request received at create_course view.")
    return render(request, 'm_dashboard.html')

 
def mentor_dashboard(request):
    user = request.user
    user_id = request.session.get('user_id')
    if not user.is_authenticated:

        return render(request, 'mentor/login.html') 
    mentor = User.objects.get(id=user_id)
    print(mentor,",,,,,,,,,,,,,,,,,,,")

    return render(request, 'm_dashboard.html', {'mentor': mentor})

 
def handle_mentees(request):
    return render(request, 'mentor/mentees.html')

#job view
# def schedule_view(request):
#     user_id = request.session.get('user_id')
#     courses = Course.objects.all(author_id=user_id)
#     return render(request, 'mentor/schedule.html', {'courses': courses})

def schedule_view(request):
    courses = Course.objects.filter(author=request.user)
    return render(request, 'schedule.html', {'courses': courses})


# # message view
# def message_view(request, ):
#     course = get_object_or_404(Course, id=course_id)
#     receiver = get_object_or_404(User, id=receiver_id) if receiver_id else None
#     sender = request.user

#     # Send message
#     if request.method == 'POST':
#         message_text = request.POST.get('message')
#         if message_text:
#             ChatMessage.objects.create(
#                 course=course,
#                 sender=sender,
#                 receiver=receiver,
#                 message=message_text
#             )
#             return redirect('mentor:message', course_id=course.id, receiver_id=receiver.id)

#     # View message history
#     messages = ChatMessage.objects.filter(
#         course=course,
#         sender__in=[sender, receiver],
#         receiver__in=[sender, receiver]
#     ).order_by('timestamp') if receiver else []

#     context = {
#         'course': course,
#         'receiver': receiver,
#         'messages': messages
#     }
#     return render(request, 'mentor/messages.html', context)



def message_view(request, course_id, receiver_id=None):
    course = get_object_or_404(Course, id=course_id)
    sender = request.user
    receiver = get_object_or_404(User, id=receiver_id) if receiver_id else None

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text and receiver:
            ChatMessage.objects.create(
                course=course,
                sender=sender,
                receiver=receiver,
                message=message_text
            )
        return redirect('mentor_app:message', course_id=course.id, receiver_id=receiver.id)

    elif request.method == 'GET' and receiver:
        messages = ChatMessage.objects.filter(
            course=course,
            sender__in=[sender, receiver],
            receiver__in=[sender, receiver]
        ).order_by('timestamp')
    else:
        messages = []

    context = {
        'course': course,
        'receiver': receiver,
        'messages': messages
    }
    return render(request, 'mentor/messages.html', context)

    
