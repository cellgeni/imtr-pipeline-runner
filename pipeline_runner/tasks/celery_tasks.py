from pipeline_runner.execution import async_run
from pipeline_runner.celery_app import celery_app


@celery_app.task()
def run_command(command: str):
    return async_run(command)
