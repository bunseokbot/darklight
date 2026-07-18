#!/usr/bin/env python3
"""Read one target's Elasticsearch document and print address candidates."""

import json
import os
import re
from configparser import ConfigParser
from urllib.parse import urlparse

import requests


config_file = os.environ.get("CONFIG_FILE", "config.ini")
config = ConfigParser()

if not config.read(config_file):
    raise SystemExit("config file not found: {}".format(config_file))

target_url = config.get("SOURCE", "ONION_URL", fallback="").strip()
parsed_target = urlparse(target_url)

if parsed_target.scheme not in ("http", "https") or not parsed_target.hostname:
    raise SystemExit("set one http(s) URL in SOURCE.ONION_URL")
if parsed_target.username or parsed_target.password:
    raise SystemExit("SOURCE.ONION_URL must not contain credentials")

try:
    target_port = parsed_target.port
except ValueError:
    raise SystemExit("SOURCE.ONION_URL contains an invalid port")

if target_port is not None:
    raise SystemExit("SOURCE.ONION_URL must not contain an explicit port")
if not parsed_target.hostname.lower().endswith(".onion"):
    raise SystemExit("SOURCE.ONION_URL must point to an .onion host")

elasticsearch_host = "localhost"
elasticsearch_port = "9200"
elasticsearch_username = config.get("ELASTICSEARCH", "USERNAME", fallback="")
elasticsearch_password = config.get("ELASTICSEARCH", "PASSWORD", fallback="")
elasticsearch_url = "http://{}:{}/webpage/_search".format(
    elasticsearch_host,
    elasticsearch_port,
)

authentication = None
if elasticsearch_username:
    authentication = (elasticsearch_username, elasticsearch_password)

query = {
    "size": 100,
    "_source": ["url", "domain", "source"],
    "query": {"term": {"url": target_url}},
}

response = requests.post(
    elasticsearch_url,
    json=query,
    auth=authentication,
    timeout=10,
)
response.raise_for_status()
hits = response.json().get("hits", {}).get("hits", [])

address_pattern = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?:(?P<btc_legacy>[13][a-km-zA-HJ-NP-Z1-9]{25,34})|"
    r"(?P<evm>0x[A-Fa-f0-9]{40}))"
    r"(?![A-Za-z0-9])"
)

seen = set()
documents_scanned = 0

for hit in hits:
    documents_scanned += 1
    document = hit.get("_source", {})
    source = document.get("source") or ""

    for match in address_pattern.finditer(source):
        address_type = "btc_legacy"
        address = match.group("btc_legacy")

        if match.group("evm"):
            address_type = "evm"
            address = match.group("evm")

        candidate = (address_type, address)
        if candidate not in seen:
            seen.add(candidate)
            print(json.dumps({
                "record": "candidate",
                "document_id": hit.get("_id"),
                "url": document.get("url"),
                "type": address_type,
                "value": address,
            }, ensure_ascii=False))

print(json.dumps({
    "record": "summary",
    "documents_scanned": documents_scanned,
    "unique_candidates": len(seen),
}, ensure_ascii=False))
