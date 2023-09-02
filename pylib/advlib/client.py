import io
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)


class AdvLibException(Exception):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("message", "unknown message"))
        self.status = kwargs.get("status", 400)


class ADVClient:
    def __init__(self, apikey=None, endpoint=None):
        self.endpoint = endpoint or os.environ.get("LABELBOX_API_URL", "https://api.labelbox.com/")
        self.apikey = apikey or self.load_api_key()

    def load_api_key(self):
        key = os.environ.get("LABELBOX_API_KEY")
        if key:
            return key

        path_to_key = os.environ.get("LABELBOX_API_KEY_FILE")
        if path_to_key:
            with(open(path_to_key, "r")) as fp:
                fp.read().strip()

        raise RuntimeError("Set API key in either LABELBOX_API_KEY or LABELBOX_API_KEY_FILE env vars")

    def post(self, path, body=None):
        return self._make_request("post", path, body)

    def get(self, path, body=None):
        return self._make_request("get", path, body)

    def delete(self, path, body=None):
        return self._make_request("delete", path, body)

    def send_ndjson(self, path, file_path, callback=None):
        """
        Sends an NDJson file in chunks.

        Args:
            path: The URL path
            file_path: The path to the NDJSON file.
            callback: A callback to run for each chunk uploaded.
        """

        def upload_chunk(_buffer, _count):
            _buffer.write(b"\n")
            _headers = {
                "Content-Type": "application/x-ndjson",
                "X-Content-Lines": str(_count),
                "Content-Length": str(buffer.tell())
            }
            rsp = self.send_bytes(path, _buffer, _headers)
            rsp.raise_for_status()
            if callback:
                callback(rsp.json())

        buffer = io.BytesIO()
        count = 0
        with open(file_path, 'rb') as fp:
            for line in fp:
                buffer.write(line)
                count += 1
                if count >= 1000:
                    upload_chunk(buffer, count)
                    buffer = io.BytesIO()
                    count = 0
        if count:
            upload_chunk(buffer, count)

    def send_bytes(self, path, buffer, headers=None):
        buffer.seek(0)
        return requests.put(self._make_url(path),
                            headers=self._headers(headers),
                            data=buffer)

    def _make_request(self, method, path, body=None, is_json=True):
        request_function = getattr(requests, method)
        if body is not None:
            data = json.dumps(body)
        else:
            data = body
        path = f"/adv/{path}"
        url = self._make_url(path)
        rsp = request_function(url, data=data, headers=self._headers())
        return self.__handle_rsp(rsp, is_json)

    def __handle_rsp(self, rsp, is_json):
        if rsp.status_code != 200:
            self._raise_exception(rsp)

        if is_json and len(rsp.content):
            rsp_val = rsp.json()
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(
                    "rsp: status: %d  body: '%s'" % (rsp.status_code, rsp_val))
            return rsp_val
        return rsp

    def _raise_exception(self, rsp):
        try:
            kwargs = rsp.json()
        except Exception as e:
            # The result is not json.
            kwargs = {
                "message": f"Your HTTP request was invalid '{rsp.status_code}',",
                f"response not JSON formatted. {e}"
                "status": rsp.status_code
            }
        raise AdvLibException(**kwargs)

    def _headers(self, merge=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "Authorization": f"Bearer {self.apikey}",
        }
        if merge:
            headers.update(merge)
        return headers

    def _make_url(self, path):
        return f"{self.endpoint}{path}"
