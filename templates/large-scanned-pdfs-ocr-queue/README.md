# Large scanned PDFs through the OCR queue

Running Docling yourself on a machine with 8 GB of RAM can fail with out of
memory errors on large PDFs, even when you split them into 2-page batches.
This template sends each whole PDF to the flatmark queue instead. Docling runs
with OCR and table recognition on flatmark's servers, and your machine only
uploads the file and downloads Markdown, so the same script runs on a laptop
or a small cloud instance.

## Run it

1. [Get your API key](https://flatmark.dev/go/tpl-large-scanned-pdfs-ocr-queue?to=/app/api-keys).
   The queue needs one.
2. Run the script with [uv](https://docs.astral.sh/uv/), which installs the
   [`flatmark`](https://pypi.org/project/flatmark/) SDK for it:

   ```bash
   export FLATMARK_API_KEY=...
   uv run convert_queue.py scans/*.pdf --json
   ```

   Or `pip install flatmark` and run it with `python convert_queue.py`.

`report.pdf` becomes `report.md` in the same folder, plus `report.json` with
`--json`: the DoclingDocument with page numbers, headings and tables.

## What it does

For each PDF, one at a time:

1. `submit_conversion_job` (`POST /v1/convert/jobs`) uploads the file and
   returns a `job_id`.
2. `get_job` (`GET /v1/jobs/{job_id}`) polls the job: first after 5 seconds,
   then with the wait doubling up to 30 seconds. On a 429 `rate_limited`
   answer it waits as long as `Retry-After` says. Polls cost no credits.
3. When `status` is `succeeded`, `get_conversion_result`
   (`GET /v1/convert/jobs/{job_id}/result`) downloads the Markdown, and with
   `--json` the JSON too. Downloads cost no credits.

A job with `status: failed` names the reason in `error`, and its credits are
refunded.

## Limits

- Up to 25 MB and 200 pages per file, and about 2 minutes of conversion. For
  a larger scan, split it into parts and submit each part.
- Each queued file costs 10 credits. Prices: https://flatmark.dev/pricing
- Results are deleted 7 days after submission.
- If you have a public endpoint, pass a `webhook_url` to
  `BodySubmitConversionJob` and skip the polling.
