from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# ...existing code...


def send_contact_form_email(name, email, subject, message):

    # Temporary localhost email backend for development
    context = {
        "is_contact_form": True,
        "survey": {
            "title": subject,
            "created_by": f"{name} ({email})",
            "description": message,
            "created_at": datetime.now()
        },
        "admin_url": f"{settings.SITE_URL}/admin/",
        "site_name": "Student Survey Platform",
    }

    try:
        html_message = render_to_string("email_template.html", context)
        msg = EmailMessage(
            subject=f"Contact Form: {subject}",
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER],
        )
        msg.content_subtype = "html"
        msg.send()
        logger.info(f"Sent contact form email from {email}")
        return True
    except Exception as e:
        logger.exception(f"Failed to send contact form email from {email}")
        return False


def notify_admin_new_survey_proposal(survey):
    subject = f"New Survey Proposal: {survey.title}"

    # Temporary localhost email backend for development
    context = {
        "survey": survey,
        "admin_url": f"{settings.SITE_URL}/admin/student_survey/survey/{survey.id}/change/",
        "site_name": "Student Survey Platform",
    }

    html_message = render_to_string("email_template.html", context)

    try:
        msg = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER],
        )
        msg.content_subtype = "html"
        msg.send()
        logger.info(f"Sent admin notification for survey ID={survey.id}")
    except Exception as e:
        logger.exception(f"Failed to send email for survey ID={survey.id}")
