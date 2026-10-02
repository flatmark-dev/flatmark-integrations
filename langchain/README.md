# langchain-flatmark

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

A LangChain document loader for the [flatmark API](https://flatmark.dev): `FlatmarkLoader` turns local files and URLs into Markdown `Document`s.

```sh
pip install langchain-flatmark
```

```python
from langchain_flatmark import FlatmarkLoader

docs = FlatmarkLoader("report.pdf").load()
print(docs[0].page_content)
```

Direct conversion (`POST /v1/convert`) works without a key at a lower rate limit. [Get an API key](https://flatmark.dev/go/langchain?to=/app/api-keys) and pass it as `api_key=` or set `FLATMARK_API_KEY`.

For large or scanned files, convert through the queue (an API key is required):

```python
loader = FlatmarkLoader(["scan.pdf", "https://example.com/deck.pptx"], use_queue=True)
for doc in loader.lazy_load():
    print(doc.metadata, len(doc.page_content))
```

The loader submits `POST /v1/convert/jobs`, polls `GET /v1/jobs/{job_id}` until the job's status is `succeeded` or `failed`, then downloads `GET /v1/convert/jobs/{job_id}/result`.

## Documents

One `Document` per source; `page_content` is the Markdown. `metadata` carries `source` (the path or URL as given) plus the `meta` fields of the answer — and `job_id` for a queued conversion.

A URL is downloaded by the loader without your key, then uploaded. Other options: `base_url`, `poll_interval`, `timeout`, and `client` (an `httpx.Client` for proxies or retries).

API reference: https://flatmark.dev/docs · Support: https://flatmark.dev/support · Generated from [`openapi.json`](../openapi.json).
