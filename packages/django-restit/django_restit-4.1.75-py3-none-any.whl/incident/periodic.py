from rest.decorators import periodic
from taskqueue.models import Task


@periodic(minute=50, hour=8)
def run_cleanup(force=False, verbose=False, now=None):
    Task.Publish("incident", "run_cleanup", channel="tq_app_handler")
