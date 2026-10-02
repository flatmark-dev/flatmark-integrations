# Documents to a RAG vector store

Turn a folder of PDF, Word, PowerPoint, Excel, HTML and text files into
heading-aware chunks for a knowledge base. flatmark converts every file to
Markdown, so one chunker handles every format. Your own embedding model and
vector store take it from there, local or hosted.

## Run it

1. [Get your API key](https://flatmark.dev/go/tpl-documents-to-rag-vector-store?to=/app/api-keys).
2. Run the script with [uv](https://docs.astral.sh/uv/), which installs the
   [`flatmark`](https://pypi.org/project/flatmark/) SDK for it:

   ```bash
   export FLATMARK_API_KEY=...
   uv run ingest.py corpus/ --out chunks.jsonl
   ```

   Or `pip install flatmark` and run it with `python ingest.py corpus/`.

## What it does

- Sends each file to `convert_document` (`POST /v1/convert`), up to 8 MB, and
  gets Markdown back.
- Splits the Markdown at headings, keeps the heading path of each chunk
  (`["Contract", "Termination"]`) as context, and caps a chunk at 4,000
  characters, cut at paragraph breaks.
- Calls `index()` with the chunks of each file. By default, `index()` appends
  them to a JSONL file, one object per chunk with `source`, `headings` and
  `text`.

## Plug in your vector store

Replace the body of `index()` in `ingest.py`: embed each `text` with your
embedding model and upsert the vector with `source` and `headings` as
metadata. Many embedding models expect a prefix for documents and a different
one for queries; check the model card. The ingestion model and the model that
answers questions can be different models.

## Files the direct call skips

The script names them on stderr:

- Files over 8 MB, and scans without a text layer (they come back empty). Send
  them to the queue, which runs OCR: see the
  [large-scanned-pdfs-ocr-queue](../large-scanned-pdfs-ocr-queue) template.
- PDFs come back from the direct call as plain text without headings, so they
  are chunked by size only. The queue returns PDF headings and tables too.

Each direct call costs 1 credit. Prices: https://flatmark.dev/pricing
