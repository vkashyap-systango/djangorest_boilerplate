from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangorest_boilerplate.settings')

from django.conf import settings  # noqa

app = Celery('djangorest_boilerplate')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.CELERYBEAT_SCHEDULE =  {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'users.tasks.temp',
        'schedule': crontab(minute='*/1'),
    },
}

# Run celery for development: celery -A djangorest_boilerplate worker -l info
