from django.urls import path
from user_app.views import register_view, login_view, \
    logout_view, user_profile, features, subscriptions, support, \
    forgot_password

app_name = 'user_app'  

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('profile/', user_profile, name='user_profile'),
    path('features/', features, name='features'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('support/', support, name='support'),
]


