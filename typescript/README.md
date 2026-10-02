# flatmark — TypeScript SDK

Document to Markdown API and MCP server for PDF, Word, PowerPoint, Excel and HTML. OCR queue for large files. Hosted in Germany.

```sh
npm install @flatmark-dev/sdk
```

[Get an API key](https://flatmark.dev/go/npm-sdk?to=/app/api-keys) and set it once:

```ts
import { client, getMe } from '@flatmark-dev/sdk';

client.setConfig({ auth: process.env.FLATMARK_API_KEY });
const { data, error } = await getMe();
```

Every operation is a function taking `{ path, query, body }`; file fields take a `Blob` or `File`. Requests go to `https://api.flatmark.dev` (`client.setConfig({ baseUrl })` to change it).

`submitConversionJob` queues a job: poll `getJob` until its `status` is `succeeded` or `failed`, then fetch `getConversionResult`.

## Operations

| Function | Endpoint | What it does |
|---|---|---|
| `getMe` | `GET /v1/me` | Your plan, remaining requests, and remaining credits |
| `getJob` | `GET /v1/jobs/{job_id}` | Get one queued job by ID |
| `listJobs` | `GET /v1/jobs` | List your queued jobs, newest first |
| `convertDocument` | `POST /v1/convert` | Convert a document to Markdown in one call |
| `submitConversionJob` | `POST /v1/convert/jobs` | Queue a document for conversion with OCR and tables |
| `getConversionResult` | `GET /v1/convert/jobs/{job_id}/result` | Download a queued job's Markdown or JSON |

Generated with @hey-api/openapi-ts from [`openapi.sdk.json`](../openapi.sdk.json). API reference: https://flatmark.dev/docs · Support: https://flatmark.dev/support
