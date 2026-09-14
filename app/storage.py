from typing import Optional
from uuid import UUID

from app.database import SessionLocal
from app.db_models import JobRecord
from app.models import Job, JobResult


def _to_pydantic(record: JobRecord) -> Job:
    return Job(
        id=record.id,
        status=record.status,
        filename=record.filename,
        raw_content=record.raw_content,
        result=JobResult(**record.result) if record.result else None,
        error=record.error,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


class JobStore:
    def create(self, job: Job) -> Job:
        with SessionLocal() as session:
            record = JobRecord(
                id=job.id,
                status=job.status.value,
                filename=job.filename,
                raw_content=job.raw_content,
                created_at=job.created_at,
                updated_at=job.updated_at,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return _to_pydantic(record)

    def get(self, job_id: UUID) -> Optional[Job]:
        with SessionLocal() as session:
            record = session.get(JobRecord, job_id)
            return _to_pydantic(record) if record else None

    def list(self) -> list[Job]:
        with SessionLocal() as session:
            records = session.query(JobRecord).order_by(JobRecord.created_at).all()
            return [_to_pydantic(r) for r in records]

    def update(self, job: Job) -> Job:
        with SessionLocal() as session:
            record = session.get(JobRecord, job.id)
            record.status = job.status.value
            record.result = job.result.model_dump() if job.result else None
            record.error = job.error
            record.updated_at = job.updated_at
            session.commit()
            session.refresh(record)
            return _to_pydantic(record)

    def clear(self) -> None:
        with SessionLocal() as session:
            session.query(JobRecord).delete()
            session.commit()


job_store = JobStore()
