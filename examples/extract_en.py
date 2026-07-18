#!/usr/bin/env python3
"""Find and print address candidates from one target's Elasticsearch documents."""

# These standard-library modules handle JSON output, environment variables,
# regular expressions, INI configuration, and URL parsing.
import json
import os
import re
from configparser import ConfigParser
from urllib.parse import urlparse

# requests is an external library used to send HTTP requests to Elasticsearch.
import requests


# Use the CONFIG_FILE environment variable, or config.ini when it is unset.
# ConfigParser stores the sections and keys read from an INI file.
config_file = os.environ.get("CONFIG_FILE", "config.ini")
config = ConfigParser()

# read() returns an empty list when it could not read any configuration file.
# SystemExit stops the script before it can run with missing settings.
if not config.read(config_file):
    raise SystemExit("config file not found: {}".format(config_file))

# Read SOURCE.ONION_URL, remove surrounding whitespace, and split the URL
# into parts such as its scheme, hostname, and port.
target_url = config.get("SOURCE", "ONION_URL", fallback="").strip()
parsed_target = urlparse(target_url)

# Require an HTTP(S) URL with a hostname before making a search request.
if parsed_target.scheme not in ("http", "https") or not parsed_target.hostname:
    raise SystemExit("set one http(s) URL in SOURCE.ONION_URL")

# Reject URLs that contain a username or password to avoid embedded credentials.
if parsed_target.username or parsed_target.password:
    raise SystemExit("SOURCE.ONION_URL must not contain credentials")

# Reading .port raises ValueError when the URL contains a non-numeric port.
# Convert that exception into a message that explains the configuration error.
try:
    target_port = parsed_target.port
except ValueError:
    raise SystemExit("SOURCE.ONION_URL contains an invalid port")

# The URL must have no explicit port, and its hostname must end in .onion.
# lower() makes the hostname check independent of letter case.
if target_port is not None:
    raise SystemExit("SOURCE.ONION_URL must not contain an explicit port")
if not parsed_target.hostname.lower().endswith(".onion"):
    raise SystemExit("SOURCE.ONION_URL must point to an .onion host")

# Read the Elasticsearch settings, using each fallback when a key is absent.
# Combine the host and port into the webpage index's search endpoint.
elasticsearch_host = config.get("ELASTICSEARCH", "HOST", fallback="elasticsearch")
elasticsearch_port = config.get("ELASTICSEARCH", "PORT", fallback="9200")
elasticsearch_username = config.get("ELASTICSEARCH", "USERNAME", fallback="")
elasticsearch_password = config.get("ELASTICSEARCH", "PASSWORD", fallback="")
elasticsearch_url = "http://{}:{}/webpage/_search".format(
    elasticsearch_host,
    elasticsearch_port,
)

# Build the basic-auth tuple expected by requests only when a username exists.
# Passing None sends the request without authentication.
authentication = None
if elasticsearch_username:
    authentication = (elasticsearch_username, elasticsearch_password)

# Search for up to 100 documents whose URL exactly matches the target.
# Limit each result's source data to the url, domain, and source fields.
query = {
    "size": 100,
    "_source": ["url", "domain", "source"],
    "query": {"term": {"url": target_url}},
}

# Send the search as JSON and set a timeout so a stalled request does not hang.
# raise_for_status() turns a 4xx or 5xx response into an exception.
response = requests.post(
    elasticsearch_url,
    json=query,
    auth=authentication,
    timeout=10,
)
response.raise_for_status()

# Extract the list of search results from the JSON response.
# Empty dictionaries and lists avoid errors when an intermediate key is absent.
hits = response.json().get("hits", {}).get("hits", [])

# The expressions at both ends keep a match out of longer alphanumeric text.
# btc_legacy has a Base58-like form; evm has 0x followed by 40 hex digits.
# This finds text shapes only; it does not validate an address or its checksum.
address_pattern = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?:(?P<btc_legacy>[13][a-km-zA-HJ-NP-Z1-9]{25,34})|"
    r"(?P<evm>0x[A-Fa-f0-9]{40}))"
    r"(?![A-Za-z0-9])"
)

# The set tracks (address type, value) pairs that were already printed.
# documents_scanned counts the search documents actually inspected.
seen = set()
documents_scanned = 0

# Read _source from each search hit and use an empty string when its body is absent.
for hit in hits:
    documents_scanned += 1
    document = hit.get("_source", {})
    source = document.get("source") or ""

    # finditer() returns every regular-expression match in the document body.
    for match in address_pattern.finditer(source):
        # Start with the Bitcoin group, then replace it if the EVM group matched.
        # The | operator means each match belongs to only one alternative.
        address_type = "btc_legacy"
        address = match.group("btc_legacy")

        if match.group("evm"):
            address_type = "evm"
            address = match.group("evm")

        # Use the type and value together as the key that prevents duplicates.
        candidate = (address_type, address)
        if candidate not in seen:
            seen.add(candidate)

            # Print one JSON line per candidate so another program can parse it.
            # ensure_ascii=False keeps non-ASCII characters instead of \u escapes.
            print(json.dumps({
                "record": "candidate",
                "document_id": hit.get("_id"),
                "url": document.get("url"),
                "type": address_type,
                "value": address,
            }, ensure_ascii=False))

# Finish with one JSON line containing the document and unique-candidate counts.
print(json.dumps({
    "record": "summary",
    "documents_scanned": documents_scanned,
    "unique_candidates": len(seen),
}, ensure_ascii=False))
