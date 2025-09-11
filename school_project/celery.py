# celery.py
import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue
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



app.conf.task_queues = (
    Queue('default', routing_key='task.default'),
    Queue('high_priority', routing_key='task.high'),
    Queue('low_priority', routing_key='task.low'),
)

app.conf.task_default_queue = 'default'
app.conf.task_default_routing_key = 'task.default'
