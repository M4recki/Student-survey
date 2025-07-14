from django.core.mail import send_mail
from django.conf import settings

def notify_admin_new_survey_proposal(survey):
    """
    Notify the admin about a new survey proposal.
    
    Args:
        survey: The survey instance that was proposed.
    """
    send_mail(
        subject=f"New Survey Proposal: {survey.title}",
        message=f"A new survey proposal has been submitted:\n\nTitle: {survey.title}, by: {survey.created_by}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
    )