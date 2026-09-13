import csv
import io
from datetime import datetime, timezone
from uuid import UUID

import pandas as pd

from app.models import ColumnSummary, JobResult, JobStatus
from app.storage import job_store


def validate_csv_structure(raw_content: str) -> list[str]:
    reader = csv.reader(io.StringIO(raw_content))
    header = next(reader, None)
    if header is None:
        return ["CSV has no header row"]

    expected_cols = len(header)
    errors = []
    for line_num, row in enumerate(reader, start=2):
        if len(row) != expected_cols:
            errors.append(
                f"Row {line_num} has {len(row)} fields, expected {expected_cols}"
            )
    return errors


def process_job(job_id: UUID) -> None:
    """Fake worker. Phase 5+ replaces this with a real Kubernetes Job."""
    job = job_store.get(job_id)
    if job is None:
        return

    job.status = JobStatus.RUNNING
    job.updated_at = datetime.now(timezone.utc)
    job_store.update(job)

    try:
        validation_errors = validate_csv_structure(job.raw_content)

        df = pd.read_csv(io.StringIO(job.raw_content))
        if df.empty:
            raise ValueError("CSV has no rows")

        columns = []
        for col in df.columns:
            series = df[col]
            is_numeric = pd.api.types.is_numeric_dtype(series)
            columns.append(
                ColumnSummary(
                    name=col,
                    dtype=str(series.dtype),
                    null_count=int(series.isna().sum()),
                    min=float(series.min()) if is_numeric else None,
                    max=float(series.max()) if is_numeric else None,
                    mean=float(series.mean()) if is_numeric else None,
                )
            )

        job.result = JobResult(
            row_count=len(df),
            column_count=len(df.columns),
            duplicate_row_count=int(df.duplicated().sum()),
            columns=columns,
            validation_errors=validation_errors,
        )
        job.status = JobStatus.COMPLETED
    except Exception as exc:
        job.status = JobStatus.FAILED
        job.error = str(exc)

    job.updated_at = datetime.now(timezone.utc)
    job_store.update(job)
