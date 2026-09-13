import time
from datetime import datetime, timezone
from uuid import UUID

from app.models import JobResult, JobStatus
from app.storage import job_store

SIMULATED_PROCESSING_SECONDS = 3


def process_job(job_id: UUID) -> None:
    """Fake worker. Phase 5+ replaces this with a real Kubernetes Job."""
    job = job_store.get(job_id)
    if job is None:
        return

    job.status = JobStatus.RUNNING
    job.updated_at = datetime.now(timezone.utc)
    job_store.update(job)

    try:
        time.sleep(SIMULATED_PROCESSING_SECONDS)
        job.result = JobResult(
            word_count=len(job.input_text.split()),
            char_count=len(job.input_text),
        )
        job.status = JobStatus.COMPLETED
    except Exception as exc:
        job.status = JobStatus.FAILED
        job.error = str(exc)

    job.updated_at = datetime.now(timezone.utc)
    job_store.update(job)
