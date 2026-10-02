# @flatmark-dev/n8n-nodes-flatmark

An [n8n](https://n8n.io) community node for the [flatmark API](https://flatmark.dev).

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

flatmark converts PDF, Word, PowerPoint, Excel and HTML to Markdown over a REST API and an MCP server. Files up to 8 MB convert in one call with MarkItDown. Files up to 25 MB and 200 pages go through a queue that runs Docling with OCR and table detection. The queue returns Markdown and a JSON structure file, by polling or a signed webhook. The servers are in Germany. The free plan has 100 credits a month and needs no card.

## Installation

In n8n, open **Settings > Community Nodes**, choose **Install** and enter `@flatmark-dev/n8n-nodes-flatmark`.

## Credentials

[Create an API key](https://flatmark.dev/go/n8n?to=/app/api-keys), then add an **flatmark API** credential in n8n and paste the key.

## Operations

| Resource | Operation | What it does |
|---|---|---|
| Account | Get Me | Your plan, remaining requests, and remaining credits |
| Job | Get Job | Get one queued job by ID |
| Job | List Jobs | List your queued jobs, newest first |
| Flatmark | Convert Document | Convert a document to Markdown in one call |
| Flatmark | Submit Conversion Job | Queue a document for conversion with OCR and tables |
| Flatmark | Get Conversion Result | Download a queued job's Markdown or JSON |

File inputs read an input binary field (default `data`). JSON answers become the item; text and XML answers come back as `data`; files as the binary field `data`. Queued jobs are polled until they finish.

## Support

https://flatmark.dev/support
