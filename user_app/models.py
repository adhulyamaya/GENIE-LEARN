from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    ]
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, null=True, blank=True)
    educational_qualification = models.CharField(max_length=50, null=True, blank=True)
    certificates = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    subscriptions_type = models.CharField(max_length=20, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    occupation = models.CharField(max_length=20, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    sub_category = models.TextField(null=True, blank=True)
    certificate_file = models.FileField(upload_to="certificates/", null=True, blank=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
