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




#         candidate = Candidate.objects.get(user_id=user_id)  
#         print(f"DEBUG: Candidate found: {candidate.user_id.email}") 
        
#         resume_data = {
#             'skills': candidate.extracted_skills,
#             'location': candidate.extracted_location,
#             'experience': candidate.extracted_experience
#         }
#         print(f"Resume data extracted: {resume_data}")
        
#         jobs = Job.objects.all()
#         print(f"Total jobs fetched: {len(jobs)}")
        
#         filtered_jobs = filter_jobs(resume_data, jobs)
#         print(f"Filtered jobs count: {len(filtered_jobs)}")
        
#         api_key = "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"
#         ranked_jobs = []
        
#         if filtered_jobs:
#             for job in filtered_jobs:
#                 print(f"Ranking job: {job.title}")
#                 score = rank_job(resume_data, job, api_key)
#                 print(f"Score for job '{job.title}': {score}")
#                 ranked_jobs.append({
#                     "job_id": job.id,
#                     "job_title": job.title,
#                     "score": score,
#                     "description": job.description[:150] + "..." if len(job.description) > 150 else job.description,
#                     "location": job.location,
#                     "job_type": job.job_type,
#                     "min_experience": job.min_experience,
#                 })
#             ranked_jobs.sort(key=lambda x: x['score'], reverse=True)
        
#         print(f"Ranked jobs sorted: {ranked_jobs}")
#         return render(request, 'jobs/suggested_jobs.html', {
#             'matched_jobs': ranked_jobs,
#             'candidate': candidate,
#             'total_jobs': len(jobs),
#             'filtered_jobs_count': len(filtered_jobs)
#         })
#     except Candidate.DoesNotExist:
#         print("Error: Candidate not found")
#         return JsonResponse({'error': 'Candidate not found'}, status=404)
    
#     except Exception as e:
#         print(f"Error in rank_jobs view: {e}")
#         messages.error(request, f"An error occurred: {str(e)}")
#         return render(request, 'candidate_home.html', {'error': str(e)})
    
