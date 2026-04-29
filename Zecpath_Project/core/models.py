from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            phone=extra_fields.get('phone', ''),
            role=extra_fields.get('role', 'candidate')
        )

        # Admin auto permissions
        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('candidate', 'Candidate'),
    )

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=255, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    company_size = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email




class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    skills = models.TextField(blank=True)
    education = models.CharField(max_length=255, blank=True)
    experience = models.FloatField(null=True, blank=True)
    expected_salary = models.IntegerField(null=True, blank=True)

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    is_active = models.BooleanField(default=True)







class Job(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)