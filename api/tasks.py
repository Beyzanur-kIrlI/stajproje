from celery import Celery
from celery.utils.log import get_task_logger
from datetime import datetime
import subprocess

from api.extensions import db
from api.models import JobResult

logger = get_task_logger(__name__)

celery = Celery(
    "tasks",
    broker="pyamqp://guest@rabbitmq//",
    backend="rpc://"
)

@celery.task
def run_shell_command_task(job_id, result_id):
    """Shell komutlarını çalıştırır."""
    logger.info(f"Running shell command for job {job_id}")
    result = JobResult.query.get(result_id)
    if not result:
        logger.error("Result not found")
        return

    try:
        process = subprocess.Popen(
            ["echo", "Hello from Shell!"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        result.status = "completed"
        result.output = out.decode() if out else err.decode()
        result.finished_at = datetime.utcnow()
        db.session.commit()

    except Exception as e:
        result.status = "failed"
        result.output = str(e)
        db.session.commit()

@celery.task
def run_katana_task(job_id, result_id):
    """Katana komutunu çalıştırır."""
    logger.info(f"Running Katana for job {job_id}")
    result = JobResult.query.get(result_id)
    if not result:
        logger.error("Result not found")
        return

    try:
        process = subprocess.Popen(
            ["echo", "Katana scan started..."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        result.status = "completed"
        result.output = out.decode() if out else err.decode()
        result.finished_at = datetime.utcnow()
        db.session.commit()

    except Exception as e:
        result.status = "failed"
        result.output = str(e)
        db.session.commit()

