
1)/recommend_courses/<user_id>/



2)Django receives the request and runs the recommend_courses view:

    *It fetches the User by user_id

    *Extracts the user's skills

    *Fetches all published Course entries

    *Builds a prompt using those skills and courses

    *Sends the prompt to GrouQ API using      call_grouq_api()

    *Returns the LLM's raw course recommendations as a JSON response




User profile: jith@gmail.com
{'skills': 'django,flask'} .................................................................
 data extracted: {'skills': 'django,flask'}
Total courses fetched: 13

Evaluating course: Python for Beginners
skills_required field: 'Python, Programming, Beginner'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: python
  ✅ Course 'Python for Beginners' MATCHED all criteria!

Evaluating course: Advanced Django
skills_required field: 'Django, Web Development, Backend, Advanced'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: django
  ✅ Course 'Advanced Django' MATCHED all criteria!

Evaluating course: Data Science with Python
skills_required field: 'Python, Data Science, Pandas, Numpy'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: python
  ✅ Course 'Data Science with Python' MATCHED all criteria!

Evaluating course: Web Development with React
skills_required field: 'React, JavaScript, Web Development, Frontend'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: web
  ✅ Course 'Web Development with React' MATCHED all criteria!

Evaluating course: Mastering SQL for Data Analysis
skills_required field: 'SQL, Database, Data Analysis'
  ❌ No matching skills found
  ❌ Course 'Mastering SQL for Data Analysis' filtered out - skill_match: False

Evaluating course: Introduction to Machine Learning
skills_required field: 'Machine Learning, Python, Data Science'
  ❌ No matching skills found
  ❌ Course 'Introduction to Machine Learning' filtered out - skill_match: False

Evaluating course: Building APIs with Django REST Framework
skills_required field: 'Django, REST API, Python, Backend'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: django
  ✅ Course 'Building APIs with Django REST Framework' MATCHED all criteria!

Evaluating course: Vue.js for Beginners
skills_required field: 'Vue.js, JavaScript, Frontend'
  ❌ No matching skills found
  ❌ Course 'Vue.js for Beginners' filtered out - skill_match: False

Evaluating course: Deep Learning with TensorFlow
skills_required field: 'Deep Learning, TensorFlow, AI, Python'
  ❌ No matching skills found
  ❌ Course 'Deep Learning with TensorFlow' filtered out - skill_match: False

Evaluating course: Agile Project Management
skills_required field: 'Project Management, Agile, Scrum'
  ❌ No matching skills found
  ❌ Course 'Agile Project Management' filtered out - skill_match: False

Evaluating course: Full Stack Web Development
skills_required field: 'MongoDB, Express, React, Node.js, Full Stack'
  ❌ No matching skills found
  ✅ Course title contains tech keyword: web
  ✅ Course 'Full Stack Web Development' MATCHED all criteria!

Evaluating course: Docker and Kubernetes for Beginners
skills_required field: 'Docker, Kubernetes, DevOps'
  ❌ No matching skills found
  ❌ Course 'Docker and Kubernetes for Beginners' filtered out - skill_match: False

Evaluating course: Introduction to Cloud Computing
skills_required field: 'Cloud Computing, AWS, Azure'
  ❌ No matching skills found
  ❌ Course 'Introduction to Cloud Computing' filtered out - skill_match: False
Filtered courses count: 6
Ranking course: Python for Beginners
Score for course 'Python for Beginners': 0
Ranking course: Advanced Django
Score for course 'Advanced Django': 60
Ranking course: Data Science with Python
Score for course 'Data Science with Python': 20
Ranking course: Web Development with React
Score for course 'Web Development with React': 20
Ranking course: Building APIs with Django REST Framework
Score for course 'Building APIs with Django REST Framework': 33
Ranking course: Full Stack Web Development
Score for course 'Full Stack Web Development': 20
Ranked courses sorted: [{'course_id': 2, 'course_title': 'Advanced Django', 'score': 60}, {'course_id': 7, 'course_title': 'Building APIs with Django REST Framework', 'score': 33}, {'course_id': 3, 'course_title': 'Data Science with Python', 'score': 20}, {'course_id': 4, 'course_title': 'Web Development with React', 'score': 20}, {'course_id': 11, 'course_title': 'Full Stack Web Development', 'score': 20}, {'course_id': 1, 'course_title': 'Python for Beginners', 'score': 0}]
[03/May/2025 15:46:13] "GET /courses_app/recommend_courses/ HTTP/1.1" 200 482    