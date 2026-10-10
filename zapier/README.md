# flatmark for Zapier

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

flatmark converts PDF, Word, PowerPoint, Excel and HTML to Markdown over a REST API and an MCP server. Files up to 8 MB convert in one call with MarkItDown. Files up to 25 MB and 200 pages go through a queue that runs Docling with OCR and table detection. The queue returns Markdown and a JSON structure file, by polling or a signed webhook. The servers are in Germany. The free plan has 100 credits a month and needs no card.

The [flatmark](https://flatmark.dev) integration for Zapier, version 1.0.4,
generated from the API's [OpenAPI document](../openapi.json). Connect it with
an API key: [create one](https://flatmark.dev/go/zapier?to=/app/api-keys).

| Action | What it does |
|---|---|
| `get_me` | Your plan, remaining requests, and remaining credits |
| `get_job` | Get one queued job by ID |
| `list_jobs` | List your queued jobs, newest first |
| `convert_document` | Convert a document to Markdown in one call |
| `submit_conversion_job` | Queue a document for conversion with OCR and tables |
| `get_conversion_result` | Download a queued job's Markdown or JSON |

## Develop

```sh
npm install
npx zapier-platform validate --without-style
API_KEY=... npm test   # live calls; without a key only the definitions are checked
```

Linked to Zapier integration `247123` (`.zapierapprc`). Releases of this repository push the version to Zapier
(`.github/workflows/publish.yml`).

Support: https://flatmark.dev/support
