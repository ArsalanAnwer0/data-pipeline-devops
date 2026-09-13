from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ColumnSummary(BaseModel):
    name: str
    dtype: str
    null_count: int
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None


class JobResult(BaseModel):
    row_count: int
    column_count: int
    duplicate_row_count: int
    columns: list[ColumnSummary]
    validation_errors: list[str] = Field(default_factory=list)


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    status: JobStatus = JobStatus.PENDING
    filename: str
    raw_content: str
    result: Optional[JobResult] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
