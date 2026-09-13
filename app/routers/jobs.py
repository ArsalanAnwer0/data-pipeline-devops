from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.models import Job, JobCreateRequest
from app.processing import process_job
from app.storage import job_store

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=Job, status_code=201)
def create_job(payload: JobCreateRequest, background_tasks: BackgroundTasks) -> Job:
    job = Job(input_text=payload.text)
    job_store.create(job)
    background_tasks.add_task(process_job, job.id)
    return job


@router.get("", response_model=list[Job])
def list_jobs() -> list[Job]:
    return job_store.list()


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: UUID) -> Job:
    job = job_store.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
