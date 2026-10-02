# /// script
# requires-python = ">=3.11"
# dependencies = ["flatmark>=1.0.0"]
# ///
"""Send large or scanned PDFs to the flatmark queue, which runs OCR and table
recognition on flatmark's servers, then save the Markdown next to each PDF.

    export FLATMARK_API_KEY=...
    uv run convert_queue.py scans/*.pdf --json

Nothing heavy runs locally: the script uploads each file, polls the job until
it has finished, and downloads the result. One file at a time, so a plan's
limit on unfinished jobs is never hit.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys
import time

import httpx
from flatmark import AuthenticatedClient
from flatmark.api.convert import get_conversion_result, submit_conversion_job
from flatmark.api.jobs import get_job
from flatmark.models import (
    BodySubmitConversionJob,
    GetConversionResultFormat,
    JobResponse,
    JobSubmitResponse,
    Problem,
)
from flatmark.types import File

QUEUE_MAX_BYTES = 25 * 1024 * 1024  # the queue also stops at 200 pages
FIRST_POLL = 5.0  # seconds before the first poll
MAX_POLL = 30.0  # the wait between polls doubles up to this
GIVE_UP = 30 * 60  # seconds; a job that is still queued then is left alone


def fail(path: pathlib.Path, resp) -> None:
    problem = resp.parsed
    if isinstance(problem, Problem):
        print(f"{path.name}: {problem.code}: {problem.detail}", file=sys.stderr)
    else:
        print(f"{path.name}: HTTP {int(resp.status_code)}", file=sys.stderr)


def wait_for(client: AuthenticatedClient, job_id: str) -> JobResponse | None:
    """Poll the job (polls cost no credits) until it succeeded or failed."""
    delay, deadline = FIRST_POLL, time.monotonic() + GIVE_UP
    while time.monotonic() < deadline:
        time.sleep(delay)
        resp = get_job.sync_detailed(job_id, client=client)
        if isinstance(resp.parsed, JobResponse):
            if resp.parsed.status in ("succeeded", "failed"):
                return resp.parsed
            delay = min(delay * 2, MAX_POLL)
        elif isinstance(resp.parsed, Problem) and resp.parsed.code == "rate_limited":
            # Polls share the per-minute rate limit: wait as long as asked.
            delay = float(resp.headers.get("Retry-After", MAX_POLL))
        else:
            return None
    return None


def convert(client: AuthenticatedClient, path: pathlib.Path, want_json: bool) -> bool:
    if path.stat().st_size > QUEUE_MAX_BYTES:
        print(f"{path.name}: over 25 MB, split it into parts first", file=sys.stderr)
        return False

    with path.open("rb") as fh:
        body = BodySubmitConversionJob(
            file=File(payload=fh, file_name=path.name, mime_type="application/pdf")
        )
        resp = submit_conversion_job.sync_detailed(client=client, body=body)
    if not isinstance(resp.parsed, JobSubmitResponse):
        fail(path, resp)
        return False
    job_id = resp.parsed.job_id
    print(f"{path.name}: queued as job {job_id}")

    job = wait_for(client, job_id)
    if job is None:
        print(f"{path.name}: no final status yet; check job {job_id} later", file=sys.stderr)
        return False
    if job.status == "failed":
        # A failed job's credits are refunded. The reason is in `error`.
        print(f"{path.name}: failed: {job.error}", file=sys.stderr)
        return False

    formats = [(GetConversionResultFormat.MARKDOWN, ".md")]
    if want_json:
        formats.append((GetConversionResultFormat.JSON, ".json"))
    for fmt, suffix in formats:
        result = get_conversion_result.sync_detailed(job_id, client=client, format_=fmt)
        if int(result.status_code) != 200:
            fail(path, result)
            return False
        path.with_suffix(suffix).write_bytes(result.content)
    print(f"{path.name}: saved {path.with_suffix('.md').name}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdfs", nargs="+", type=pathlib.Path)
    parser.add_argument("--json", action="store_true", help="also save the DoclingDocument JSON")
    args = parser.parse_args()

    client = AuthenticatedClient(
        base_url="https://api.flatmark.dev",
        token=os.environ["FLATMARK_API_KEY"],
        auth_header_name="X-API-Key",
        prefix="",
        timeout=httpx.Timeout(120.0),
    )
    ok = [convert(client, pdf, args.json) for pdf in args.pdfs]
    sys.exit(0 if all(ok) else 1)


if __name__ == "__main__":
    main()
