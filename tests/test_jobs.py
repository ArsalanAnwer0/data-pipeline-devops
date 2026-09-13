import io
import time

VALID_CSV = "name,age,score\nalice,30,85.5\nbob,25,90.0\n"
MALFORMED_CSV = "a,b,c\n1,2\n"


def _wait_for_completion(client, job_id, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        response = client.get(f"/jobs/{job_id}")
        body = response.json()
        if body["status"] in ("completed", "failed"):
            return body
        time.sleep(0.1)
    raise TimeoutError(f"Job {job_id} did not finish within {timeout}s")


def test_create_job_returns_pending(client):
    response = client.post(
        "/jobs",
        files={"file": ("sample.csv", io.BytesIO(VALID_CSV.encode()), "text/csv")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["filename"] == "sample.csv"


def test_job_completes_with_correct_stats(client):
    response = client.post(
        "/jobs",
        files={"file": ("sample.csv", io.BytesIO(VALID_CSV.encode()), "text/csv")},
    )
    job_id = response.json()["id"]

    result = _wait_for_completion(client, job_id)

    assert result["status"] == "completed"
    assert result["result"]["row_count"] == 2
    assert result["result"]["column_count"] == 3
    assert result["result"]["validation_errors"] == []


def test_malformed_csv_reports_validation_error(client):
    response = client.post(
        "/jobs",
        files={"file": ("broken.csv", io.BytesIO(MALFORMED_CSV.encode()), "text/csv")},
    )
    job_id = response.json()["id"]

    result = _wait_for_completion(client, job_id)

    assert result["status"] == "completed"
    assert result["result"]["validation_errors"] == ["Row 2 has 2 fields, expected 3"]


def test_rejects_non_csv_file(client):
    response = client.post(
        "/jobs",
        files={"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert response.status_code == 400


def test_get_unknown_job_returns_404(client):
    response = client.get("/jobs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_jobs_returns_created_jobs(client):
    client.post(
        "/jobs",
        files={"file": ("sample.csv", io.BytesIO(VALID_CSV.encode()), "text/csv")},
    )
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.json()) == 1
