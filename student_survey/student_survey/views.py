from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def signup(request):
    return render(request, "signup.html")


def login(request):
    return render(request, "login.html")


def survey(request):
    return render(request, "survey.html")


def about(request):
    return render(request, "about.html")
