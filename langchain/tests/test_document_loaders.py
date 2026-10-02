"""Tests for langchain_flatmark, against an httpx.MockTransport (no network)."""

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import httpx

from langchain_flatmark import FlatmarkLoader, FlatmarkError
from langchain_flatmark.document_loaders import (
    AUTH_HEADER,
    BASE_URL,
    CONVERT_PATH,
    JOB_ID,
    META_FIELD,
    POLL_PATH,
    RESULT_PATH,
    SUBMIT_PATH,
    TEXT_FIELD,
)

AT = "{" + JOB_ID + "}"


class Api:
    """A fake flatmark API: records requests, answers by path."""

    def __init__(self, statuses=("running", "succeeded"), error=None):
        self.requests, self.statuses, self.error = [], list(statuses), error

    def __call__(self, request):
        request.read()
        self.requests.append(request)
        path = request.url.path
        if request.url.host == "files.example.com":
            return httpx.Response(200, content=b"%PDF-1.7 remote", headers={"content-type": "application/pdf"})
        if self.error:
            return httpx.Response(self.error, json={"detail": "nope"})
        if path.endswith(CONVERT_PATH):
            answer = {TEXT_FIELD: "# Hello"}
            if META_FIELD:
                answer[META_FIELD] = {"filename": "a.pdf", "title": "Hello"}
            return httpx.Response(200, json=answer)
        if path.endswith(SUBMIT_PATH):
            return httpx.Response(202, json={JOB_ID: "j1", "status": "queued"})
        if path.endswith(POLL_PATH.replace(AT, "j1")):
            status = self.statuses.pop(0)
            return httpx.Response(200, json={"id": "j1", "status": status, "error": "too big" if status == "failed" else None})
        if path.endswith(RESULT_PATH.replace(AT, "j1")):
            return httpx.Response(200, text="# Queued", headers={"content-type": "text/markdown"})
        return httpx.Response(404, json={"detail": path})


class LoaderTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pdf = Path(tmp.name) / "a.pdf"
        self.pdf.write_bytes(b"%PDF-1.7 local")
        env = mock.patch.dict(os.environ, {}, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def loader(self, api, source=None, **kwargs):
        client = httpx.Client(transport=httpx.MockTransport(api))
        self.addCleanup(client.close)
        return FlatmarkLoader(source or str(self.pdf), client=client, poll_interval=0, **kwargs)

    def test_direct_convert_is_anonymous_without_a_key(self):
        api = Api()
        [doc] = self.loader(api).load()
        self.assertEqual(doc.page_content, "# Hello")
        self.assertEqual(doc.metadata["source"], str(self.pdf))
        [request] = api.requests
        self.assertEqual(str(request.url), BASE_URL + CONVERT_PATH)
        self.assertNotIn(AUTH_HEADER.lower(), request.headers)
        self.assertIn(b'filename="a.pdf"', request.content)
        self.assertIn(b"Content-Type: application/pdf", request.content)

    def test_key_from_argument_or_environment(self):
        api = Api()
        self.loader(api, api_key="k1").load()
        os.environ["FLATMARK_API_KEY"] = "k2"
        self.loader(api).load()
        self.assertEqual([r.headers[AUTH_HEADER] for r in api.requests], ["k1", "k2"])

    def test_url_is_fetched_without_the_key(self):
        api = Api()
        url = "https://files.example.com/papers/b.pdf"
        [doc] = self.loader(api, url, api_key="k1").load()
        fetch, convert = api.requests
        self.assertNotIn(AUTH_HEADER.lower(), fetch.headers)
        self.assertEqual(convert.headers[AUTH_HEADER], "k1")
        self.assertIn(b'filename="b.pdf"', convert.content)
        self.assertEqual(doc.metadata["source"], url)

    def test_several_sources_one_document_each(self):
        docs = self.loader(Api(), [str(self.pdf), self.pdf]).load()
        self.assertEqual(len(docs), 2)

    def test_queue_submits_polls_and_downloads(self):
        api = Api()
        [doc] = self.loader(api, api_key="k1", use_queue=True).load()
        self.assertEqual(doc.page_content, "# Queued")
        self.assertEqual(doc.metadata, {"source": str(self.pdf), JOB_ID: "j1"})
        paths = [r.url.path for r in api.requests]
        self.assertEqual(
            paths,
            [SUBMIT_PATH, POLL_PATH.replace(AT, "j1"), POLL_PATH.replace(AT, "j1"), RESULT_PATH.replace(AT, "j1")],
        )

    def test_failed_job_raises(self):
        with self.assertRaisesRegex(FlatmarkError, "too big"):
            self.loader(Api(statuses=["failed"]), api_key="k1", use_queue=True).load()

    def test_queue_needs_a_key(self):
        with self.assertRaisesRegex(ValueError, "API key"):
            FlatmarkLoader(str(self.pdf), use_queue=True)

    def test_api_error_raises_with_status(self):
        with self.assertRaisesRegex(FlatmarkError, "429"):
            self.loader(Api(error=429)).load()

    def test_async_load(self):
        docs = asyncio.run(self.loader(Api()).aload())
        self.assertEqual(docs[0].page_content, "# Hello")


if __name__ == "__main__":
    unittest.main()
