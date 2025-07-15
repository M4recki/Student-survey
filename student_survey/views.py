from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.mail import send_mail
from json import dumps
from .models import Student, Survey, Question, Choice, Answer, Response
from .utils import notify_admin_new_survey_proposal
from django.conf import settings
from datetime import datetime, timedelta


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

    if request.method == "POST":
        survey_id = request.POST.get("survey_id")
        survey = Survey.objects.get(id=survey_id)
        survey.delete()
        messages.success(request, "Survey deleted successfully.")
        return redirect("survey")

    for survey in surveys:
        survey.has_responded = survey.user_has_responded(request.user)  # type: ignore
        survey.response_count = survey.get_response_count()  # type: ignore

    return render(request, "survey.html", {"surveys": surveys})


@login_required
def create_survey(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        survey = Survey.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            is_approved=False,
        )

        # Add questions
        idx = 0
        while True:
            q_text = request.POST.get(f"questions[{idx}][text]")
            q_type = request.POST.get(f"questions[{idx}][type]")
            if not q_text:
                break
            question = Question.objects.create(
                survey=survey, text=q_text, question_type=q_type
            )
            if q_type != "text":
                options = request.POST.getlist(f"questions[{idx}][options][]")
                for opt in options:
                    if opt.strip():
                        Choice.objects.create(question=question, text=opt)
            idx += 1

        notify_admin_new_survey_proposal(survey)
        messages.success(request, "Survey created successfully.")
        return redirect("survey")
    return render(request, "create_survey.html")


@user_passes_test(lambda u: u.is_superuser)
def manage_surveys(request):
    surveys = Survey.objects.filter(is_approved=False).prefetch_related(
        "questions__choices"
    )
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

            Question.objects.filter(survey=survey).delete()

            # Add new questions
            idx = 0
            while True:
                q_text = request.POST.get(f"questions[{idx}][text]")
                q_type = request.POST.get(f"questions[{idx}][type]")
                if not q_text:
                    break

                question = Question.objects.create(
                    survey=survey, text=q_text, question_type=q_type
                )

                if q_type != "text":
                    options = request.POST.getlist(f"questions[{idx}][options][]")
                    for opt in options:
                        if opt.strip():
                            Choice.objects.create(question=question, text=opt)
                idx += 1

            messages.success(request, "Survey updated successfully.")
            survey.save()
            messages.success(request, "Survey updated successfully.")
        elif action == "delete":
            survey.delete()
            messages.success(request, "Survey deleted successfully.")
        return redirect("manage_surveys")
    return render(request, "manage_surveys.html", {"surveys": surveys})


@user_passes_test(lambda u: u.is_superuser)
def admin_stats(request):
    # Basic statistics
    total_surveys = Survey.objects.count()
    total_responses = Response.objects.count()
    total_users = Student.objects.count()
    active_users = Response.objects.values("student").distinct().count()
    avg_response_rate = round(
        (total_responses / total_surveys) * 100 if total_surveys > 0 else 0, 1
    )

    # Data for charts
    chart_data = {
        "responseDates": [],
        "responseCounts": [],
        "popularSurveyLabels": [],
        "popularSurveyCounts": [],
        "questionTypeCounts": [0, 0, 0],  # radio, checkbox, text
        "userActivityData": {
            "activeUsers": active_users,
            "totalUsers": total_users,
        },
    }

    # Responses over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    responses_by_date = (
        Response.objects.filter(submitted_at__gte=thirty_days_ago)
        .annotate(date=TruncDate("submitted_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    # Fill in all dates
    current_date = thirty_days_ago.date()
    end_date = timezone.now().date()

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        count = next(
            (
                item["count"]
                for item in responses_by_date
                if item["date"].strftime("%Y-%m-%d") == date_str
            ),
            0,
        )
        chart_data["responseDates"].append(date_str)
        chart_data["responseCounts"].append(count)
        current_date += timedelta(days=1)

    # Popular surveys
    popular_surveys = Survey.objects.annotate(
        response_count=Count("responses")
    ).order_by("-response_count")[:5]

    chart_data["popularSurveyLabels"] = [s.title for s in popular_surveys]
    chart_data["popularSurveyCounts"] = [s.response_count for s in popular_surveys]  # type: ignore

    # Question type distribution
    for qt in Question.objects.values("question_type").annotate(count=Count("id")):
        if qt["question_type"] == "radio":
            chart_data["questionTypeCounts"][0] = qt["count"]
        elif qt["question_type"] == "checkbox":
            chart_data["questionTypeCounts"][1] = qt["count"]
        elif qt["question_type"] == "text":
            chart_data["questionTypeCounts"][2] = qt["count"]

    context = {
        "total_surveys": total_surveys,
        "total_responses": total_responses,
        "total_users": total_users,
        "active_users": active_users,
        "avg_response_rate": avg_response_rate,
        "chart_data": dumps(chart_data),
    }

    return render(request, "admin_stats.html", context)


@login_required
def take_survey(request, survey_id):
    survey = Survey.objects.get(id=survey_id)

    if Response.objects.filter(survey=survey, student=request.user).exists():
        messages.error(request, "You have already completed this survey.")
        return redirect("survey")

    questions = survey.questions.all().order_by(  # type: ignore
        models.Case(
            models.When(question_type="radio", then=0),
            models.When(question_type="checkbox", then=1),
            models.When(question_type="text", then=2),
            default=3,
            output_field=models.IntegerField(),
        ),
        "order",
    )

    if request.method == "POST":
        response = Response.objects.create(survey=survey, student=request.user)

        for question in questions:
            if question.question_type == "text":
                answer_text = request.POST.get(f"question_{question.id}")
                if answer_text:
                    Answer.objects.create(
                        response=response, question=question, text=answer_text
                    )
            elif question.question_type == "checkbox":
                choice_ids = request.POST.getlist(f"question_{question.id}[]")
                for choice_id in choice_ids:
                    Answer.objects.create(
                        response=response, question=question, choice_id=choice_id
                    )
            else:  # radio
                choice_id = request.POST.get(f"question_{question.id}")
                if choice_id:
                    Answer.objects.create(
                        response=response, question=question, choice_id=choice_id
                    )

        messages.success(request, "Survey completed successfully!")
        return redirect("survey")

    return render(
        request, "take_survey.html", {"survey": survey, "questions": questions}
    )


def about(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        send_mail(
            subject=f"Contact Form: {subject} | From: {name} <{email}>",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        messages.success(request, "Your message has been sent successfully.")
        return redirect("about")

    return render(request, "about.html")
