from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Student(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Survey(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="surveys"
    )

    def user_has_responded(self, user):
        return Response.objects.filter(survey=self, student=user).exists()

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("radio", "Single choice"),
        ("checkbox", "Multiple choice"),
        ("text", "Text response"),
    ]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['question_type', 'order']

    def save(self, *args, **kwargs):
        # Automatic order assignment
        if not self.order:
            if self.question_type == 'text':
                last_order = Question.objects.filter(survey=self.survey).aggregate(models.Max('order'))['order__max']
                self.order = (last_order or 0) + 1000
            else:
                last_order = Question.objects.filter(
                    survey=self.survey, 
                    question_type=self.question_type
                ).aggregate(models.Max('order'))['order__max']
                self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    response = models.ForeignKey(
        Response, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=True)
