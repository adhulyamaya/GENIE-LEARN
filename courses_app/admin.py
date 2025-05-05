from django.contrib import admin
from .models import Course, Lesson, Enrollment,Quiz, Question, QuizResult

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'category', 'price', 'is_published', 'created_at')
    search_fields = ('title', 'author__email', 'category')
    list_filter = ('difficulty', 'is_published', 'category')
    ordering = ('-created_at',)
    fields = ('title', 'description', 'skills', 'author', 'thumbnail', 'difficulty', 'category', 'tags', 'price', 'is_published')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizResult)

