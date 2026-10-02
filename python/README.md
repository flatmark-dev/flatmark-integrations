# flatmark — Python SDK

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

```sh
pip install flatmark
```

[Get an API key](https://flatmark.dev/go/pypi-sdk?to=/app/api-keys) and pass it to the client:

```python
import os

from flatmark import AuthenticatedClient
from flatmark.api.account import get_me

client = AuthenticatedClient(
    base_url="https://api.flatmark.dev",
    token=os.environ["FLATMARK_API_KEY"],
    auth_header_name="X-API-Key",
    prefix="",
)
print(get_me.sync(client=client))
```

Every operation is a module with `sync`, `sync_detailed`, `asyncio` and `asyncio_detailed`; file fields take a `flatmark.types.File(payload=..., file_name=..., mime_type=...)`.

`submit_conversion_job` queues a job: poll `get_job` until its `status` is `succeeded` or `failed`, then fetch `get_conversion_result`.

## Operations

| Operation | Module | What it does |
|---|---|---|
| `GET /v1/me` | `flatmark.api.account.get_me` | Your plan, remaining requests, and remaining credits |
| `GET /v1/jobs/{job_id}` | `flatmark.api.jobs.get_job` | Get one queued job by ID |
| `GET /v1/jobs` | `flatmark.api.jobs.list_jobs` | List your queued jobs, newest first |
| `POST /v1/convert` | `flatmark.api.convert.convert_document` | Convert a document to Markdown in one call |
| `POST /v1/convert/jobs` | `flatmark.api.convert.submit_conversion_job` | Queue a document for conversion with OCR and tables |
| `GET /v1/convert/jobs/{job_id}/result` | `flatmark.api.convert.get_conversion_result` | Download a queued job's Markdown or JSON |

Generated with openapi-python-client from [`openapi.sdk.json`](../openapi.sdk.json). API reference: https://flatmark.dev/docs · Support: https://flatmark.dev/support
