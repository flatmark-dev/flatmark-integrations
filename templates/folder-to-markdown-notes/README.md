# Folder of PDFs to Markdown notes (n8n)

An n8n workflow that turns a folder of PDFs, such as lecture notes or
exported handouts, into Markdown notes in your Obsidian vault. Text, headings
and tables arrive as Markdown, so you can link and edit them instead of
copying text out of each PDF by hand. Scanned pages are read with OCR.

## Set it up

You need a self-hosted n8n, version 2.33 or later: the workflow reads and
writes files on the machine that runs n8n. Every node ships with n8n, so there
is nothing to install.

1. [Get your API key](https://flatmark.dev/go/tpl-folder-to-markdown-notes?to=/app/api-keys).
2. Import `workflow.json` (**Workflows > Import from file**).
3. Open *Queue the PDF* and create a **Header Auth** credential with the name
   `X-API-Key` and your key as the value. Pick the same credential in *Check
   the job* and *Download Markdown*.
4. Make the folders visible to n8n. The workflow reads
   `/home/node/.n8n-files/pdf-inbox/*.pdf` and writes to
   `/home/node/.n8n-files/vault/`, the default `~/.n8n-files` of the n8n
   Docker image. Mount your folders there, for example
   `-v ~/pdf-inbox:/home/node/.n8n-files/pdf-inbox -v ~/Obsidian/MyVault/PDF\ notes:/home/node/.n8n-files/vault`,
   or change the paths in the *Read PDFs* and *Save note to vault* nodes and
   add them to `N8N_RESTRICT_FILE_ACCESS_TO`.
5. Click **Execute workflow**. `notes.pdf` becomes `notes.md` in the vault folder.

## The nodes

| Node | What it does |
| --- | --- |
| When clicking 'Execute workflow' | Starts a run by hand |
| Read PDFs | Reads every PDF in the inbox folder |
| One PDF at a time | Loop Over Items, batch size 1: hands on the next PDF once the last one is done |
| Queue the PDF | HTTP Request: `POST https://api.flatmark.dev/v1/convert/jobs` with the PDF as the multipart field `file` (`submit_conversion_job`) |
| Wait 5 seconds | Waits before each status check |
| Check the job | HTTP Request: `GET https://api.flatmark.dev/v1/jobs/{job_id}` (`get_job`) |
| Job status | Switch on `status`: `succeeded` goes on to the download, `failed` skips to the next PDF, anything else waits again |
| Download Markdown | HTTP Request: `GET https://api.flatmark.dev/v1/convert/jobs/{job_id}/result` (`get_conversion_result`), the Markdown as text in `data` |
| Markdown to file | Turns the Markdown text into a `.md` file named after the PDF |
| Save note to vault | Writes the note into the vault folder, then hands back to *One PDF at a time* |

The three HTTP Request nodes use **Authentication** Generic Credential Type
with the same Header Auth credential. They read the job id from *Queue the
PDF* and the file name from *One PDF at a time*, so each PDF keeps its own
job while the status check repeats.

## Good to know

- Each run converts every PDF in the inbox folder. Move converted PDFs out
  before the next run.
- The queue takes files up to 25 MB and 200 pages. Each file costs 10 credits,
  refunded if the job fails. Status checks and downloads are free. Prices:
  https://flatmark.dev/pricing
- A failed job is skipped, and the workflow goes on with the next PDF.
- Images are not extracted, only text and tables. To keep the figures, put the
  PDF in the vault too and embed it in the note with `![[notes.pdf]]`.
- For PDFs with a text layer and no tables, the direct call costs 1 credit,
  but it returns plain text without headings or tables. To switch, replace the
  queue steps with one HTTP Request node that POSTs the PDF as the multipart
  field `file` to `https://api.flatmark.dev/v1/convert`. Its JSON answer has
  the text in `markdown`, so set the *Text Input Field* of *Markdown to file*
  to `markdown`.
