from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from user_app.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages


from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        print("Received POST request for registration.")
        try:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            subscriptions_type = request.POST.get('subscriptions_type')
            educational_qualification = request.POST.get('educational_qualification')
            certificates = request.FILES.get('certificates')

            if password1 != password2:
                messages.error(request, "Passwords do not match!")
                return redirect('user_app:register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('user_app:register')

            user = User.objects.create_user(
                email=email,
                password=password1,
                full_name=full_name,
                phone=phone,
                gender=gender,
                subscriptions_type=subscriptions_type,
                educational_qualification=educational_qualification,
                certificate_file=certificates
            )

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')

        except IntegrityError:
            messages.error(request, "A database error occurred. Please try again.")
        except Exception as e:
            print("Unexpected error:", e)
            messages.error(request, f"Unexpected error: {str(e)}")

    print("Rendering registration form.")
    return render(request, 'register.html')





# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, "Login successful!")
#             return redirect('users:user_profile')  
#         else:
#             messages.error(request, "Invalid username or password")
#     else:
#         form = AuthenticationForm()

#     return render(request, 'users/login.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Login attempt with email: {email}")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.full_name}!")
            return redirect('landing') 

            # return JsonResponse({
            #     'status': 'success',
            #     'message': f"Welcome, {user.full_name}!",
            #     'redirect_url': '/home'
            # })
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('index') 
            # return JsonResponse({
            #     'status': 'error',
            #     'message': "Invalid email or password."
            # })

    # return JsonResponse({
    #     'status': 'error',
    #     'message': 'POST request expected for login.'
    # })
    return redirect('index')






# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index') 


@login_required
def user_profile(request):
    profile, created = User.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'user_profile.html', context)


def subscriptions(request):
    return render(request, "subscriptions.html")


def support(request):
    return render(request, "support.html")


def features(request):
    return render(request, "features.html")


def forgot_password(request):
    return render(request, "forgot_password.html")