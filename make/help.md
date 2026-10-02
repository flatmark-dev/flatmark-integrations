# flatmark

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

flatmark converts PDF, Word, PowerPoint, Excel and HTML to Markdown over a REST API and an MCP server. Files up to 8 MB convert in one call with MarkItDown. Files up to 25 MB and 200 pages go through a queue that runs Docling with OCR and table detection. The queue returns Markdown and a JSON structure file, by polling or a signed webhook. The servers are in Germany. The free plan has 100 credits a month and needs no card.

## Connect

Create an API key at [flatmark.dev](https://flatmark.dev/go/make?to=/app/api-keys) and paste it
into a new flatmark connection.

## Modules

- **Your plan, remaining requests, and remaining credits**
- **Get one queued job by ID**
- **List your queued jobs, newest first**
- **Convert a document to Markdown in one call**
- **Queue a document for conversion with OCR and tables**: Returns a job ID: get the output with “Download a queued job's Markdown or JSON” once “Get one queued job by ID” reports the job done.
- **Download a queued job's Markdown or JSON**: Takes the job ID from “Queue a document for conversion with OCR and tables”.

Support: https://flatmark.dev/support
