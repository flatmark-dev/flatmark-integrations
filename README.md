# flatmark integrations

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

flatmark converts PDF, Word, PowerPoint, Excel and HTML to Markdown over a REST API and an MCP server. Files up to 8 MB convert in one call with MarkItDown. Files up to 25 MB and 200 pages go through a queue that runs Docling with OCR and table detection. The queue returns Markdown and a JSON structure file, by polling or a signed webhook. The servers are in Germany. The free plan has 100 credits a month and needs no card.

Official integrations for the [flatmark API](https://flatmark.dev), generated from its [OpenAPI document](openapi.json) and published from this repository.

## Get an API key

[Create a key](https://flatmark.dev/go/connectors?to=/app/api-keys) and send it in the `X-API-Key` header.

## Integrations

- **n8n** — community node [`@flatmark-dev/n8n-nodes-flatmark`](https://www.npmjs.com/package/@flatmark-dev/n8n-nodes-flatmark), install it under Settings → Community Nodes
- **Python SDK** — `pip install flatmark` · [PyPI](https://pypi.org/project/flatmark/)
- **TypeScript SDK** — `npm install @flatmark-dev/sdk` · [npm](https://www.npmjs.com/package/@flatmark-dev/sdk)
- **GitHub Action** — [`flatmark-dev/flatmark-action`](https://github.com/marketplace/actions/flatmark-api) on the GitHub Marketplace
- **LangChain document loader (`FlatmarkLoader`)** — `pip install langchain-flatmark` · [PyPI](https://pypi.org/project/langchain-flatmark/)

## Templates

Ready-made automations on the API: the walkthrough on the site, the files in this repository.

| Template | Platform | Walkthrough | Files |
|---|---|---|---|
| Documents to a RAG vector store | Code | [flatmark.dev/templates/documents-to-rag-vector-store](https://flatmark.dev/templates/documents-to-rag-vector-store) | [templates/documents-to-rag-vector-store](templates/documents-to-rag-vector-store) |
| Large scanned PDFs through the OCR queue | Code | [flatmark.dev/templates/large-scanned-pdfs-ocr-queue](https://flatmark.dev/templates/large-scanned-pdfs-ocr-queue) | [templates/large-scanned-pdfs-ocr-queue](templates/large-scanned-pdfs-ocr-queue) |
| Folder of PDFs to Markdown notes with n8n | n8n | [flatmark.dev/templates/folder-to-markdown-notes](https://flatmark.dev/templates/folder-to-markdown-notes) | [templates/folder-to-markdown-notes](templates/folder-to-markdown-notes) |

## Operations

| Operation | Endpoint | What it does |
|---|---|---|
| `get_me` | `GET /v1/me` | Your plan, remaining requests, and remaining credits |
| `get_job` | `GET /v1/jobs/{job_id}` | Get one queued job by ID |
| `list_jobs` | `GET /v1/jobs` | List your queued jobs, newest first |
| `convert_document` | `POST /v1/convert` | Convert a document to Markdown in one call |
| `submit_conversion_job` | `POST /v1/convert/jobs` | Queue a document for conversion with OCR and tables |
| `get_conversion_result` | `GET /v1/convert/jobs/{job_id}/result` | Download a queued job's Markdown or JSON |

API reference: https://flatmark.dev/docs · Base URL: `https://api.flatmark.dev`

## Support

https://flatmark.dev/support

Every file listed in `.generated` is rebuilt from the live API; changes to them are overwritten.
