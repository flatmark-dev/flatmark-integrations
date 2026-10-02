# flatmark for Make

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

The [flatmark](https://flatmark.dev) custom app for Make, version 1.0.2,
generated from the API's [OpenAPI document](../openapi.json). Connect it with
an API key: [create one](https://flatmark.dev/go/make?to=/app/api-keys).

| Module | What it does |
|---|---|
| `getMe` | Your plan, remaining requests, and remaining credits |
| `getJob` | Get one queued job by ID |
| `listJobs` | List your queued jobs, newest first |
| `convertDocument` | Convert a document to Markdown in one call |
| `submitConversionJob` | Queue a document for conversion with OCR and tables |
| `getConversionResult` | Download a queued job's Markdown or JSON |

## Layout

- `app.json`: the app, its connection and modules (`deploy.sh` reads it);
- `base.imljson`, `groups.json`, `help.md`: the app's base, module groups and help;
- `connection/`: the API-key connection's `parameters` and `api`;
- `modules/<name>/`: each module's `api`, `expect` (mappable parameters),
  `interface` and `samples`.

## Publish

Linked to the Make app `flatmark-n8qrcj`. Releases of this repository run `deploy.sh`
(`.github/workflows/publish.yml`), which needs
[make-cli](https://www.npmjs.com/package/@makehq/cli) 1.4.0, `jq`,
`MAKE_API_KEY` and `MAKE_ZONE`. The app logo (a 512 px PNG) is set by hand in
Make's app settings.

Support: https://flatmark.dev/support
