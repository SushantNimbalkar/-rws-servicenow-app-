"""Minimal ServiceNow Table API client.

Usage:
  python sn.py get    <table> [query] [fields] [limit]
  python sn.py create <table> '<json>'
  python sn.py update <table> <sys_id> '<json>'

Reads SN_INSTANCE, SN_USER and SN_PASS from the environment (or a local .env).
"""
import json
import os
import sys

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

H = {"Accept": "application/json", "Content-Type": "application/json"}
TIMEOUT = 60


def _config():
    missing = [k for k in ("SN_INSTANCE", "SN_USER", "SN_PASS") if not os.environ.get(k)]
    if missing:
        sys.exit("Missing environment variables: " + ", ".join(missing))
    base = os.environ["SN_INSTANCE"].rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    return base, (os.environ["SN_USER"], os.environ["SN_PASS"])


def _ok(r):
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:500]}")
    try:
        return r.json()["result"]
    except (ValueError, KeyError):
        # A hibernating PDI returns an HTML page instead of JSON.
        sys.exit("Unexpected non-JSON response (is the PDI asleep?): " + r.text[:300])


def get(table, query="", fields="", limit="20"):
    base, auth = _config()
    return _ok(requests.get(
        f"{base}/api/now/table/{table}", auth=auth, headers=H, timeout=TIMEOUT,
        params={"sysparm_query": query, "sysparm_fields": fields,
                "sysparm_limit": limit, "sysparm_display_value": "false"}))


def create(table, data):
    base, auth = _config()
    return _ok(requests.post(f"{base}/api/now/table/{table}", auth=auth, headers=H,
                             json=data, timeout=TIMEOUT))


def update(table, sys_id, data):
    base, auth = _config()
    return _ok(requests.patch(f"{base}/api/now/table/{table}/{sys_id}", auth=auth,
                              headers=H, json=data, timeout=TIMEOUT))


if __name__ == "__main__":
    commands = {"get": get, "create": create, "update": update}
    if len(sys.argv) < 3 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    cmd, table, *rest = sys.argv[1:]
    args = [json.loads(a) if a.strip().startswith("{") else a for a in rest]
    print(json.dumps(commands[cmd](table, *args), indent=2))
