from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

api_key = "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"

def rank_skills(request):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("user:login")
    return render(request, 'rank_skills.html')



