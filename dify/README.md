# flatmark

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

flatmark converts PDF, Word, PowerPoint, Excel and HTML to Markdown over a REST API and an MCP server. Files up to 8 MB convert in one call with MarkItDown. Files up to 25 MB and 200 pages go through a queue that runs Docling with OCR and table detection. The queue returns Markdown and a JSON structure file, by polling or a signed webhook. The servers are in Germany. The free plan has 100 credits a month and needs no card.

A Dify tool plugin for the [flatmark API](https://flatmark.dev).

## Setup

1. Install **flatmark** from the Dify Marketplace (Plugins → Marketplace).
2. [Create an API key](https://flatmark.dev/go/dify?to=/app/api-keys).
3. Open the plugin's tool settings, choose **Authorize** and paste the key as the flatmark API key credential.

## Usage

Add the tools to a workflow, chatflow or agent. File inputs take a Dify file; JSON object and array inputs take JSON text. JSON answers come back as JSON, text and XML as text, documents as files. A tool that queues a job returns its id: poll it with the job tool, then fetch its result with the matching result tool.

| Tool | Endpoint | What it does |
|---|---|---|
| Get me | `GET /v1/me` | Your plan, remaining requests, and remaining credits |
| Get job | `GET /v1/jobs/{job_id}` | Get one queued job by ID |
| List jobs | `GET /v1/jobs` | List your queued jobs, newest first |
| Convert document | `POST /v1/convert` | Convert a document to Markdown in one call |
| Submit conversion job | `POST /v1/convert/jobs` | Queue a document for conversion with OCR and tables |
| Get conversion result | `GET /v1/convert/jobs/{job_id}/result` | Download a queued job's Markdown or JSON |

## Connection

The plugin connects to `https://api.flatmark.dev` over HTTPS and sends the API key in the `X-API-Key` header; the Dify instance needs outbound network access to that endpoint. API reference: https://flatmark.dev/docs

## Source and support

Source repository: https://github.com/flatmark-dev/flatmark-integrations/tree/main/dify

Support: https://flatmark.dev/support
