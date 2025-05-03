from django.urls import path
from . import views

app_name = 'score_board'  # Namespace for better URL handling

urlpatterns = [
    path('scorecards/', views.scorecards, name='scorecards'),
    

]



