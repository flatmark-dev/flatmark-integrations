# Folder of PDFs to Markdown notes (n8n)

An n8n workflow that turns a folder of PDFs, such as lecture notes or
exported handouts, into Markdown notes in your Obsidian vault. Text, headings
and tables arrive as Markdown, so you can link and edit them instead of
copying text out of each PDF by hand. Scanned pages are read with OCR.

## Set it up

You need a self-hosted n8n: the workflow reads and writes files on the machine
that runs n8n.

1. In n8n, open **Settings > Community nodes** and install
   `@flatmark-dev/n8n-nodes-flatmark`.
2. [Get your API key](https://flatmark.dev/go/tpl-folder-to-markdown-notes?to=/app/api-keys).
3. Import `workflow.json` (**Workflows > Import from file**) and add the key as
   a **flatmark API** credential on the *Convert with flatmark* node.
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
| Convert with flatmark | Operation *Submit Conversion Job*: queues each PDF (`submit_conversion_job`), polls the job (`get_job`) and downloads the Markdown (`get_conversion_result`) |
| Markdown to file | Turns the Markdown text into a `.md` file named after the PDF |
| Save note to vault | Writes the note into the vault folder |

## Good to know

- Each run converts every PDF in the inbox folder. Move converted PDFs out
  before the next run.
- The queue takes files up to 25 MB and 200 pages. Each file costs 10 credits,
  refunded if the job fails. Prices: https://flatmark.dev/pricing
- Images are not extracted, only text and tables. To keep the figures, put the
  PDF in the vault too and embed it in the note with `![[notes.pdf]]`.
- For PDFs with a text layer and no tables, the *Convert Document*
  operation (the direct call) costs 1 credit, but it returns plain text without
  headings or tables. It returns the text in `markdown`, so set the *Text Input
  Field* of *Markdown to file* to `markdown` if you switch.
