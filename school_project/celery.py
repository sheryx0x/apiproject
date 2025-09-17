# celery.py
import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')

app = Celery('school_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    
    'generate-pdf-every-minute': {
        'task': 'api.tasks.generate_pdf_task',
        'schedule': crontab(minute='*/1'), 
        'args': (1,),  
    },
}



app.conf.task_queues = (
    Queue('high_priority', Exchange('tasks'), routing_key='task.high'),
    Queue('default', Exchange('tasks'), routing_key='task.default'),
    Queue('low_priority', Exchange('tasks'), routing_key='task.low'),
)

app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_routing_key = 'task.default'

# Recommended for fairness in heavy jobs:
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True