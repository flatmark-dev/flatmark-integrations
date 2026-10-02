# /// script
# requires-python = ">=3.11"
# dependencies = ["flatmark>=1.0.0"]
# ///
"""Convert a folder of documents to Markdown with flatmark, split the Markdown
at headings, and hand each chunk to your embedding model and vector store.

    export FLATMARK_API_KEY=...
    uv run ingest.py corpus/ --out chunks.jsonl

Without changes, the chunks are written to a JSONL file (one object per chunk,
with its source file and heading path). Replace ``index()`` to embed and store
them instead.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time

import httpx
from flatmark import AuthenticatedClient
from flatmark.api.convert import convert_document
from flatmark.models import BodyConvertDocument, Problem, SyncConvertResponse
from flatmark.types import File

# The direct call reads the Content-Type of the file part, so every file is
# sent with its real type.
TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".html": "text/html",
    ".htm": "text/html",
    ".txt": "text/plain",
}
DIRECT_MAX_BYTES = 8 * 1024 * 1024  # larger files go to the queue
MAX_CHARS = 4000  # cap per chunk; long sections are split at paragraph breaks
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def to_markdown(client: AuthenticatedClient, path: pathlib.Path) -> str | None:
    """One direct call. Returns None (and says why) when the file needs the queue."""
    body = BodyConvertDocument(
        file=File(
            payload=path.open("rb"),
            file_name=path.name,
            mime_type=TYPES[path.suffix.lower()],
        )
    )
    for _attempt in range(5):
        body.file.payload.seek(0)
        resp = convert_document.sync_detailed(client=client, body=body)
        if isinstance(resp.parsed, Problem) and resp.parsed.code == "rate_limited":
            # Per-minute rate limit: wait as long as the API asks, then retry.
            # Other 429s (an empty credit balance, say) are not retried.
            time.sleep(int(resp.headers.get("Retry-After", "10")))
            continue
        break
    body.file.payload.close()
    if isinstance(resp.parsed, SyncConvertResponse):
        return resp.parsed.markdown
    if isinstance(resp.parsed, Problem):
        print(f"  {path.name}: {resp.parsed.code}: {resp.parsed.detail}", file=sys.stderr)
    else:
        print(f"  {path.name}: HTTP {int(resp.status_code)}", file=sys.stderr)
    return None


def chunk(markdown: str) -> list[tuple[list[str], str]]:
    """Split at Markdown headings; keep each chunk's heading path for context."""
    sections: list[tuple[list[str], list[str]]] = []
    path: list[str] = []
    lines: list[str] = []
    for line in markdown.splitlines():
        heading = HEADING.match(line)
        if heading:
            if lines:
                sections.append((list(path), lines))
            level = len(heading.group(1))
            path = path[: level - 1] + [heading.group(2).strip()]
            lines = []
        lines.append(line)
    if lines:
        sections.append((list(path), lines))

    chunks = []
    for heading_path, body in sections:
        text = "\n".join(body).strip()
        while len(text) > MAX_CHARS:
            cut = text.rfind("\n\n", 0, MAX_CHARS)
            cut = cut if cut > 0 else MAX_CHARS
            chunks.append((heading_path, text[:cut].strip()))
            text = text[cut:].strip()
        if text:
            chunks.append((heading_path, text))
    return chunks


def index(records: list[dict], out: pathlib.Path) -> None:
    """PLUG IN YOUR EMBEDDINGS AND VECTOR STORE HERE.

    ``records`` holds one dict per chunk: ``source``, ``headings`` and ``text``.
    For example, embed ``r["text"]`` with your local embedding model and upsert
    the vector with ``source`` and ``headings`` as metadata. Many embedding
    models expect a document prefix on the text; check your model's card.

    The default writes the chunks to a JSONL file, which most vector stores and
    RAG tools can load.
    """
    with out.open("a", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("chunks.jsonl"))
    args = parser.parse_args()

    client = AuthenticatedClient(
        base_url="https://api.flatmark.dev",
        token=os.environ["FLATMARK_API_KEY"],
        auth_header_name="X-API-Key",
        prefix="",
        timeout=httpx.Timeout(120.0),
    )
    for path in sorted(args.folder.rglob("*")):
        if path.suffix.lower() not in TYPES or not path.is_file():
            continue
        if path.stat().st_size > DIRECT_MAX_BYTES:
            print(f"  {path.name}: over 8 MB, send it to the queue", file=sys.stderr)
            continue
        markdown = to_markdown(client, path)
        if markdown is None:
            continue
        if not markdown.strip():
            print(f"  {path.name}: no text layer (a scan?), send it to the queue for OCR")
            continue
        records = [
            {"source": str(path), "headings": headings, "text": text}
            for headings, text in chunk(markdown)
        ]
        index(records, args.out)
        print(f"{path.name}: {len(records)} chunks")


if __name__ == "__main__":
    main()
