import requests
import os
import json
from groq import Groq

GROUQ_API_KEY = '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'


def filter_courses(user_skills, courses):
    """Filter courses based on skills, prioritizing skills field."""
    import ast
    filtered_courses = []
    
    if isinstance(user_skills['skills'], str):
        try:
            skills = ast.literal_eval(user_skills['skills'])
        except (ValueError, SyntaxError):
            skills = [user_skills['skills']] 
    else:
        skills = user_skills['skills'] if user_skills['skills'] else []
    
    for course in courses:
        print(f"\nEvaluating job: {course.title}")
        print(f"skills_required field: '{course.skills}'")
       
        skill_match = False
        
        if course.skills.strip():
            for skill in skills:
                if skill.lower() in course.skills.lower():
                    skill_match = True
                    print(f"  ✅ Skill match found: {skill}")
                    break
            
            if not skill_match:
                print(f"  ❌ No matching skills found")
        else:
            skill_match = True
            print(f"  ✅ No skills specified for job - considering as match")
        
        if not skill_match:
            for skill in skills:
                if skill.lower() in courses.title.lower():
                    skill_match = True
                    print(f"  ✅ Job title contains skill: {skill}")
                    break
            
            if not skill_match:
                tech_keywords = ['python', 'django', 'developer', 'engineer', 'programmer', 
                               'software', 'web', 'fullstack', 'full stack', 'back end', 
                               'front end', 'javascript', 'react', 'node']
                              
                for keyword in tech_keywords:
                    if keyword.lower() in courses.title.lower():
                        skill_match = True
                        print(f"  ✅ course title contains tech keyword: {keyword}")
                        break
        if skill_match:
            print(f"  ✅ Job '{courses.title}' MATCHED all criteria!")
            filtered_courses.append(courses)
        else:
            print(f"  ❌ Job '{courses.title}' filtered out - skill_match:{skill_match},")
    
    return filtered_courses


def rank_course(user_skills, course, api_key):
    """Rank a course matches with user skills using Groq LLM."""
    client = Groq(api_key=api_key)
    
    prompt = f"""
    i wants to know which course is best suited for them based on their skills .

    Course Title: {course.title}
    Course Description: {course.description}
    Course Skills: {', '.join(course.get_skills())}
    Course Difficulty: {course.difficulty}
    Course Category: {course.category}
    Course Tags: {course.tags}
    Course Subscription: {course.subscription}
    Course Price: {course.price}

    User Details:
    Skills: {', '.join(user_skills['skills'])}

    Based on the match between the skills of the user  and course  details and skill sets, assign a score from 0 to 100.
    Consider skills match, relevance, and overall fit. Analyzing should be strict and fair.

    Return ONLY a valid JSON object with the following structure:
    {{
        "score": X
    }}
    where X is a number between 0 and 100.
    """
    
    try:
        # Call the Groq API with the updated prompt
        completion = client.chat.completions.create(
            messages=[{
                "role": "system", 
                "content": "you wants to know which courses are suitable for you based on skills. Always respond with valid JSON."
            },
            {
                "role": "user", 
                "content": prompt
            }],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
            temperature=0.5,
        )
        
        # Parse the response and get the score
        content = completion.choices[0].message.content
        data = json.loads(content)
        return data.get("score", 0)
        
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return 0
