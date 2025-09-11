# celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')

app = Celery('school_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Example task running every minute
    'generate-pdf-every-minute': {
        'task': 'api.tasks.generate_pdf_task',
        'schedule': crontab(minute='*/1'),  # every minute
        'args': (1,),  # example user_id 1
    },
}