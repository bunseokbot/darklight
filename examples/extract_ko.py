#!/usr/bin/env python3
"""한 대상의 Elasticsearch 문서에서 주소 후보를 찾아 출력한다."""

# JSON 출력, 환경 변수 조회, 정규식 검색에 필요한 표준 라이브러리다.
# ConfigParser는 INI 설정을, urlparse는 URL의 구성 요소를 다룬다.
import json
import os
import re
from configparser import ConfigParser
from urllib.parse import urlparse

# requests는 Elasticsearch에 HTTP 요청을 보내는 외부 라이브러리다.
import requests


# CONFIG_FILE 환경 변수가 없으면 현재 경로의 config.ini를 사용한다.
# ConfigParser 객체는 INI 파일의 섹션과 키를 읽어 저장한다.
config_file = os.environ.get("CONFIG_FILE", "config.ini")
config = ConfigParser()

# read()가 빈 목록을 반환하면 읽은 설정 파일이 없다는 뜻이다.
# SystemExit를 발생시켜 이후 코드가 잘못된 설정으로 실행되지 않게 한다.
if not config.read(config_file):
    raise SystemExit("config file not found: {}".format(config_file))

# SOURCE 섹션의 ONION_URL을 읽고 양끝 공백을 제거한다.
# urlparse()는 URL을 스킴, 호스트, 포트 등의 부분으로 나눈다.
target_url = config.get("SOURCE", "ONION_URL", fallback="").strip()
parsed_target = urlparse(target_url)

# http(s) URL이며 호스트 이름이 있는지 먼저 확인한다.
# 조건을 만족하지 않으면 검색 요청 전에 프로그램을 종료한다.
if parsed_target.scheme not in ("http", "https") or not parsed_target.hostname:
    raise SystemExit("set one http(s) URL in SOURCE.ONION_URL")

# 사용자 이름이나 비밀번호가 URL에 포함되면 안전을 위해 거부한다.
if parsed_target.username or parsed_target.password:
    raise SystemExit("SOURCE.ONION_URL must not contain credentials")

# port 속성을 읽을 때 숫자가 아닌 포트가 있으면 ValueError가 발생한다.
# 이를 사용자가 이해하기 쉬운 종료 메시지로 바꾼다.
try:
    target_port = parsed_target.port
except ValueError:
    raise SystemExit("SOURCE.ONION_URL contains an invalid port")

# 명시적인 포트가 없어야 하며, 호스트 이름은 .onion으로 끝나야 한다.
# lower()를 사용하므로 대소문자 차이는 검사 결과에 영향을 주지 않는다.
if target_port is not None:
    raise SystemExit("SOURCE.ONION_URL must not contain an explicit port")
if not parsed_target.hostname.lower().endswith(".onion"):
    raise SystemExit("SOURCE.ONION_URL must point to an .onion host")

# ELASTICSEARCH 설정값을 읽되, 키가 없으면 fallback의 기본값을 쓴다.
# HOST와 PORT를 조합해 webpage 인덱스의 검색 API 주소를 만든다.
elasticsearch_host = "localhost"
elasticsearch_port = "9200"
elasticsearch_username = config.get("ELASTICSEARCH", "USERNAME", fallback="")
elasticsearch_password = config.get("ELASTICSEARCH", "PASSWORD", fallback="")
elasticsearch_url = "http://{}:{}/webpage/_search".format(
    elasticsearch_host,
    elasticsearch_port,
)

# 사용자 이름이 있을 때만 requests가 사용할 기본 인증 튜플을 만든다.
# 이름이 없으면 None을 전달해 인증 없이 요청한다.
authentication = None
if elasticsearch_username:
    authentication = (elasticsearch_username, elasticsearch_password)

# 정확히 같은 URL을 가진 문서를 최대 100개까지 찾는 검색 조건이다.
# 응답의 문서 데이터는 url, domain, source 세 필드로 제한한다.
query = {
    "size": 100,
    "_source": ["url", "domain", "source"],
    "query": {"term": {"url": target_url}},
}

# 검색 조건을 JSON 본문으로 보내고 오래 멈추지 않도록 타임아웃을 설정한다.
# raise_for_status()는 4xx 또는 5xx 응답을 예외로 처리한다.
response = requests.post(
    elasticsearch_url,
    json=query,
    auth=authentication,
    timeout=10,
)
response.raise_for_status()

# JSON 응답에서 검색 결과 목록을 꺼낸다.
# 중간 키가 없을 때는 빈 딕셔너리나 빈 목록을 사용해 오류를 피한다.
hits = response.json().get("hits", {}).get("hits", [])

# 정규식 양끝은 후보가 더 긴 영숫자 문자열의 일부가 되는 것을 막는다.
# btc_legacy는 1/3으로 시작하는 Base58 모양, evm은 0x와 40자리 16진수 모양이다.
# 문자열 형식만 찾으며 실제 주소나 체크섬의 유효성까지 검증하지는 않는다.
address_pattern = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?:(?P<btc_legacy>[13][a-km-zA-HJ-NP-Z1-9]{25,34})|"
    r"(?P<evm>0x[A-Fa-f0-9]{40}))"
    r"(?![A-Za-z0-9])"
)

# set은 이미 출력한 (주소 종류, 주소 값) 쌍을 빠르게 확인한다.
# documents_scanned는 실제로 확인한 검색 문서 수를 센다.
seen = set()
documents_scanned = 0

# 각 검색 결과에서 _source 필드를 꺼내고, 본문이 없으면 빈 문자열을 쓴다.
for hit in hits:
    documents_scanned += 1
    document = hit.get("_source", {})
    source = document.get("source") or ""

    # finditer()는 본문에서 정규식과 일치한 모든 위치를 차례로 반환한다.
    for match in address_pattern.finditer(source):
        # 먼저 Bitcoin 그룹의 값을 읽고, EVM 그룹이 일치했으면 값을 바꾼다.
        # 두 패턴은 |로 연결되어 있으므로 한 번의 일치는 한 종류에 해당한다.
        address_type = "btc_legacy"
        address = match.group("btc_legacy")

        if match.group("evm"):
            address_type = "evm"
            address = match.group("evm")

        # 종류와 값을 하나의 튜플로 묶어 같은 후보의 중복 출력을 막는다.
        candidate = (address_type, address)
        if candidate not in seen:
            seen.add(candidate)

            # 후보 한 개를 JSON 한 줄로 출력해 다른 프로그램이 읽기 쉽게 한다.
            # ensure_ascii=False는 비ASCII 문자를 \u 형식으로 바꾸지 않는다.
            print(json.dumps({
                "record": "candidate",
                "document_id": hit.get("_id"),
                "url": document.get("url"),
                "type": address_type,
                "value": address,
            }, ensure_ascii=False))

# 처리한 문서 수와 중복을 제외한 후보 수를 마지막 JSON 줄로 출력한다.
print(json.dumps({
    "record": "summary",
    "documents_scanned": documents_scanned,
    "unique_candidates": len(seen),
}, ensure_ascii=False))
