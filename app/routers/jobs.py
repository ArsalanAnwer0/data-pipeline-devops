from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.models import Job
from app.processing import process_job
from app.storage import job_store

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=Job, status_code=201)
async def create_job(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
) -> Job:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    raw_bytes = await file.read()
    job = Job(filename=file.filename, raw_content=raw_bytes.decode("utf-8"))
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
