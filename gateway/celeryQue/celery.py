import os
import celery

app = celery.Celery(
    'MyQueue',
    broker = 'redis://localhost:6379/0',
    include = ['celeryQue.tasks']
)

os.environ.setdefault('DJANGO_STTINGS_MODUL', '../../gateway/settings.py')

if __name__ == "__main__":
    app.start()