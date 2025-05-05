from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from user_app.models import User
from django.db.models import Sum

    
class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    SUBSCRIPTION_CHOICES = [
    ('FREE', 'Free'),
    ('PRO', 'Pro'),
    ('PREMIUM', 'Premium'),
]
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField(null=True, blank=True)  # Comma-separated skills
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    category = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=False)
    subscription = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='FREE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_skills(self):
        return [skill.strip() for skill in self.skills.split(',')] if self.skills else []



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='lesson_videos/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)
    completed_lessons = models.ManyToManyField('Lesson', blank=True)
    score = models.IntegerField(default=0)


    class Meta:
        unique_together = ('user', 'course')

    def update_progress(self):
        total_lessons = self.course.lessons.count()
        completed_lessons = self.completed_lessons.count()
        if total_lessons > 0:
            self.progress = (completed_lessons / total_lessons) * 100
        self.save()

    def get_total_quiz_score(self):
        lessons = self.course.lessons.all()
        quizzes = Quiz.objects.filter(lesson__in=lessons)
        total_score = QuizResult.objects.filter(user=self.user, quiz__in=quizzes).aggregate(total=Sum('score'))['total'] or 0
        return total_score    
    
    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"Quiz for {self.lesson.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return self.question_text


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name} - {self.quiz.title} - {self.score}/{self.total}'




 

class ChatMessage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chat_messages')  
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True, blank=True)  
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)  
    message = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.sender if self.sender else self.receiver} to {self.receiver if self.receiver else self.sender} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
