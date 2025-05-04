from django.shortcuts import render

# # Create your views here.
# def scorecards(request):
#     return render(request, "scorecards.html")


from django.shortcuts import render

def scorecards(request):
    candidates = [
        {'name': 'Bob Williams', 'score': 92, 'exp': 3, 'domain': 'Backend Dev'},
        {'name': 'Charlie Lee', 'score': 89, 'exp': 2, 'domain': 'Data Analyst'},
        {'name': 'Diana Prince', 'score': 87, 'exp': 5, 'domain': 'Frontend Dev'},
        {'name': 'Evan Green', 'score': 85, 'exp': 1, 'domain': 'DevOps'},
        {'name': 'Fiona Smith', 'score': 82, 'exp': 4, 'domain': 'ML Engineer'},
        {'name': 'George Brown', 'score': 80, 'exp': 3, 'domain': 'QA Tester'},
    ]

    top_candidate = {
        'name': 'Alice Johnson',
        'score': 98,
        'exp': 4,
        'domain': 'Full Stack Developer',
    }

    return render(request, 'scorecards.html', {
        'top_candidate': top_candidate,
        'candidates': candidates
    })
