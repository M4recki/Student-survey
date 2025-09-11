from django.core.mail import send_mail, EmailMessage, get_connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def notify_admin_new_survey_proposal(survey):
    """
    Notify the admin about a new survey proposal.

    Args:
        survey: The survey instance that was proposed.
    """
    subject = f"New Survey Proposal: {survey.title}"
    message = f"A new survey proposal has been submitted: \n\nTitle: {survey.title}, by: {survey.created_by}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [settings.EMAIL_HOST_USER]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
        )
    except Exception as e:
        logger.exception(
            "Failed to send admin notification email for survey id=%s",
            getattr(survey, "id", "unknown"),
        )
        # Fallback: try to output the email to console (DEBUG/dev)
        try:
            conn = get_connection("django.core.mail.backends.console.EmailBackend")
            EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipients,
                connection=conn,
            ).send(fail_silently=True)
        except Exception:
            logger.exception(
                "Fallback console email also failed for survey id=%s",
                getattr(survey, "id", "unknown"),
            )
