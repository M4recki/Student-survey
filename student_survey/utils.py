from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def notify_admin_new_survey_proposal(survey):
    subject = f"New Survey Proposal: {survey.title}"
    message = f"A new survey proposal has been submitted:\n\nTitle: {survey.title}\nBy: {survey.created_by}"
    from_email = settings.DEFAULT_FROM_EMAIL
    # Prefer ADMINS if set, otherwise fallback to EMAIL_HOST_USER or DEFAULT_FROM_EMAIL
    recipients = [addr for _, addr in getattr(settings, "ADMINS", []) if addr]
    if not recipients:
        if getattr(settings, "EMAIL_HOST_USER", ""):
            recipients = [settings.EMAIL_HOST_USER]
        elif getattr(settings, "DEFAULT_FROM_EMAIL", ""):
            recipients = [settings.DEFAULT_FROM_EMAIL]

    if not recipients:
        logger.warning("No admin recipient configured for survey notifications. Set settings.ADMINS or EMAIL_HOST_USER/DEFAULT_FROM_EMAIL.")
        return

    logger.info("Sending admin notification to %s for survey id=%s", recipients, getattr(survey, "id", "unknown"))

    try:
        conn = get_connection()  # uses EMAIL_BACKEND from settings
        email = EmailMessage(subject=subject, body=message, from_email=from_email, to=recipients, connection=conn)
        email.send(fail_silently=False)
        logger.info("Admin notification sent successfully to %s", recipients)
    except Exception:
        logger.exception("Failed to send admin notification via configured backend; falling back to console backend for survey id=%s", getattr(survey, "id", "unknown"))
        try:
            conn = get_connection("django.core.mail.backends.console.EmailBackend")
            EmailMessage(subject=subject, body=message, from_email=from_email, to=recipients, connection=conn).send(fail_silently=True)
            logger.info("Fallback console email outputted for recipients %s", recipients)
        except Exception:
            logger.exception("Fallback console backend also failed for survey id=%s", getattr(survey, "id", "unknown"))