from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render

from .models import Student, Survey


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "signup.html")

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "signup.html")

        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            is_active=True,
            is_staff=False,
            date_joined=datetime.now(),
        )
        student.save()

        auth_login(request, student)

        messages.success(request, "Account created successfully.")
        return redirect("home")

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "login.html")

        student = authenticate(request, email=email, password=password)

        if student is not None:
            auth_login(request, student)

            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

            messages.success(request, "Logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")


@login_required
def survey(request):
    surveys = Survey.objects.filter(is_approved=True)
    return render(request, "survey.html", {"surveys": surveys})


@login_required
def create_survey(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.method.get("description")
        Survey.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            is_approved=request.user.is_superuser,
        )
        messages.success(request, "Survey created successfully.")
        return redirect("survey")
    return render(request, "create_survey.html")


@user_passes_test(lambda u: u.is_superuser)
def manage_surveys(request):
    surveys = Survey.objects.filter(is_approved=False)
    if request.method == "POST":
        survey_id = request.POST.get("survey_id")
        action = request.POST.get("action")
        survey = Survey.objects.get(id=survey_id)

        if action == "approve":
            survey.is_approved = True
            survey.save()
            messages.success(request, "Survey approved successfully.")
        elif action == "edit":
            title = request.POST.get("title")
            description = request.POST.get("description")
            survey.title = title
            survey.description = description
            survey.save()
            messages.success(request, "Survey updated successfully.")
        elif action == "delete":
            survey.delete()
            messages.success(request, "Survey deleted successfully.")
        return redirect("manage_surveys")
    return render(request, "manage_surveys.html", {"surveys": surveys})


def about(request):
    return render(request, "about.html")
