from django.shortcuts import render
from courses_app.models import Enrollment

# def scorecards(request):
#     candidates = [
#         {'name': 'Bob Williams', 'score': 92, 'exp': 3, 'domain': 'Backend Dev'},
#         {'name': 'Charlie Lee', 'score': 89, 'exp': 2, 'domain': 'Data Analyst'},
#         {'name': 'Diana Prince', 'score': 87, 'exp': 5, 'domain': 'Frontend Dev'},
#         {'name': 'Evan Green', 'score': 85, 'exp': 1, 'domain': 'DevOps'},
#         {'name': 'Fiona Smith', 'score': 82, 'exp': 4, 'domain': 'ML Engineer'},
#         {'name': 'George Brown', 'score': 80, 'exp': 3, 'domain': 'QA Tester'},
#     ]

#     top_candidate = {
#         'name': 'Alice Johnson',
#         'score': 98,
#         'exp': 4,
#         'domain': 'Full Stack Developer',
#     }

#     return render(request, 'scorecards.html', {
#         'top_candidate': top_candidate,
#         'candidates': candidates
#     })



# def scorecards(request):
#     enrollments = Enrollment.objects.select_related('user', 'course').all().order_by('-score')

#     if enrollments:
#         top_candidate = enrollments[0]
#         other_candidates = enrollments[1:]
#     else:
#         top_candidate = None
#         other_candidates = []

#     return render(request, 'scorecards.html', {
#         'top_candidate': top_candidate,
#         'candidates': other_candidates
#     })


def scorecards(request):
    print("Fetching all enrollments...")
    enrollments = Enrollment.objects.select_related('user', 'course').all()
    print(f"Total enrollments fetched: {len(enrollments)}")

    for enrollment in enrollments:
        enrollment.total_quiz_score = enrollment.get_total_quiz_score()
        print(f"User: {enrollment.user.full_name}, Course: {enrollment.course.title}, Total Score: {enrollment.total_quiz_score}")

    enrollments = sorted(enrollments, key=lambda x: x.total_quiz_score, reverse=True)

    if enrollments:
        top_candidate = enrollments[0]
        print(f"Top Candidate: {top_candidate.user.full_name}, Score: {top_candidate.total_quiz_score}")
        other_candidates = enrollments[1:]
    else:
        print("No enrollments found.")
        top_candidate = None
        other_candidates = []

    return render(request, 'scorecards.html', {
        'top_candidate': top_candidate,
        'candidates': other_candidates
    })
