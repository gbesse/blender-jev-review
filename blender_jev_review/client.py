"""Small standard-library Jev client with bounded retry and redacted errors."""

import json
import time
import urllib.error
import urllib.request

from .core import validate_response

ENDPOINT = "https://api.typesafe.ai/v1/systemone"


def call_jev(request, api_key, endpoint=ENDPOINT, timeout=30, retries=2):
    if not api_key.strip():
        raise ValueError("enter a TypeSafe API key")
    if not endpoint.startswith("https://") and not endpoint.startswith(("http://127.0.0.1:", "http://localhost:")):
        raise ValueError("endpoint must use HTTPS except on loopback")
    body = json.dumps(request).encode("utf-8")
    for attempt in range(retries + 1):
        http_request = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(http_request, timeout=timeout) as response:
                return validate_response(json.load(response), request["questions"])
        except urllib.error.HTTPError as error:
            if error.code in (429, 529) and attempt < retries:
                time.sleep(0.25 * (2**attempt))
                continue
            detail = error.read(160).decode("utf-8", "replace").replace(api_key, "[redacted]")
            raise RuntimeError(f"Jev HTTP {error.code}: {detail}") from error
        except urllib.error.URLError as error:
            if attempt < retries:
                time.sleep(0.25 * (2**attempt))
                continue
            raise RuntimeError(f"Jev network error: {error.reason}") from error
    raise RuntimeError("Jev request failed")

