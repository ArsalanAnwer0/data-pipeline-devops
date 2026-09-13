import threading
from typing import Dict, Optional
from uuid import UUID

from app.models import Job


class JobStore:
    """In-memory job store. Phase 2 replaces this with PostgreSQL."""

    def __init__(self) -> None:
        self._jobs: Dict[UUID, Job] = {}
        self._lock = threading.Lock()

    def create(self, job: Job) -> Job:
        with self._lock:
            self._jobs[job.id] = job
        return job

    def get(self, job_id: UUID) -> Optional[Job]:
        with self._lock:
            return self._jobs.get(job_id)

    def list(self) -> list[Job]:
        with self._lock:
            return list(self._jobs.values())

    def update(self, job: Job) -> Job:
        with self._lock:
            self._jobs[job.id] = job
        return job

    def clear(self) -> None:
        with self._lock:
            self._jobs.clear()


job_store = JobStore()
