from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def survey(request):
    return render(request, 'survey.html')

def about(request):
    return render(request, 'about.html')