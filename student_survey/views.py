from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Student


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

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "login.html")

        student = authenticate(request, email=email, password=password)

        if student is not None:
            auth_login(request, student)
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
    return render(request, "survey.html")


def about(request):
    return render(request, "about.html")
