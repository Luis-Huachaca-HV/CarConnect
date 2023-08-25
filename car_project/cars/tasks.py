# tasks.py
# tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Document

@shared_task
def send_document_reminder(user_email):
    user_documents = Document.objects.filter(car__user__email=user_email)
    
    # Calculate the date 1 month from now
    due_date_threshold = timezone.now() + timedelta(days=30)

    almost_due_documents = user_documents.filter(due_date__lte=due_date_threshold)

    for document in almost_due_documents:
        subject = f"Reminder: Your document '{document.title}' is almost due"
        message = f"Your document '{document.title}' is almost due. Please take action."
        recipient_list = [user_email]

        send_mail(subject, message, "your_email@example.com", recipient_list)
# tasks.py (update this file)
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Update with your broker URL

CELERY_BEAT_SCHEDULE = {
    'send-document-reminder': {
        'task': 'your_app.tasks.send_document_reminder',
        'schedule': crontab(minute=0, hour=0),  # Run every day at midnight
    },
}
