from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def notify_admin_new_survey_proposal(survey):
    subject = f"New Survey Proposal: {survey.title}"
    
    # Temporary localhost email backend for development
    context = {
        'survey': survey,
        'admin_url': f"{settings.SITE_URL}/admin/student_survey/survey/{survey.id}/change/",
        'site_name': "Student Survey Platform"
    }
    
    html_message = render_to_string('email_template.html', context)
    
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