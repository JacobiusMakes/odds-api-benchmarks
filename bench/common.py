"""Shared helpers for all probes. Stdlib only, so `python3` or `uv run` both work."""
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "odds-api-benchmarks/1.0 (+https://github.com/JacobiusMakes/odds-api-benchmarks)"
TIMEOUT = 15


def load_vendors():
    with open(ROOT / "data" / "vendors.json") as f:
        return json.load(f)["vendors"]


def fetch(url, method="GET", max_bytes=65536, head_bytes=2048):
    """Fetch a URL without following cross-host auth flows. Returns a dict of
    everything a probe needs: status, elapsed seconds, content type, body head."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(max_bytes)
            elapsed = time.perf_counter() - start
            return {
                "url": url,
                "status": resp.status,
                "elapsed_s": round(elapsed, 4),
                "content_type": resp.headers.get("Content-Type", ""),
                "body_head": body[:head_bytes].decode("utf-8", errors="replace"),
                "error": None,
            }
    except urllib.error.HTTPError as e:
        body = e.read(2048)
        return {
            "url": url,
            "status": e.code,
            "elapsed_s": round(time.perf_counter() - start, 4),
            "content_type": e.headers.get("Content-Type", "") if e.headers else "",
            "body_head": body.decode("utf-8", errors="replace"),
            "error": None,
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "elapsed_s": round(time.perf_counter() - start, 4),
            "content_type": "",
            "body_head": "",
            "error": f"{type(e).__name__}: {e}",
        }


def looks_like_json(result):
    ct = (result.get("content_type") or "").lower()
    head = (result.get("body_head") or "").lstrip()
    return "json" in ct or head[:1] in ("{", "[")


def write_result(out_dir, name, payload):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"wrote {path}")
