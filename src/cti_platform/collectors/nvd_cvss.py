import os
import time

import requests

from cti_platform.models import CvssInfo

NVD_CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
REQUEST_TIMEOUT_SECONDS = 30
ANONYMOUS_REQUEST_DELAY_SECONDS = 6  # API 키 없을 때 안전한 호출 간격


def fetch_cvss(cve_id: str) -> CvssInfo | None:
    """CVE의 CVSS 점수를 NVD에서 조회한다. 아직 분석 전이면 None을 반환한다."""
    api_key = os.getenv("NVD_API_KEY")
    headers = {"apiKey": api_key} if api_key else {}

    response = requests.get(
        NVD_CVE_API_URL,
        params={"cveId": cve_id},
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()

    if not api_key:
        time.sleep(ANONYMOUS_REQUEST_DELAY_SECONDS)

    vulnerabilities = payload.get("vulnerabilities", [])
    if not vulnerabilities:
        return None

    metrics = vulnerabilities[0]["cve"].get("metrics", {})
    for key, label in (("cvssMetricV31", "3.1"), ("cvssMetricV30", "3.0"), ("cvssMetricV2", "2.0")):
        if metrics.get(key):
            data = metrics[key][0]["cvssData"]
            return CvssInfo(version=label, base_score=data["baseScore"], base_severity=data.get("baseSeverity", "UNKNOWN"))

    return None