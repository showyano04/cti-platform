import os
import time
import requests
from cve_platform.models import CvssInfo

NVD_CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
REQUEST_TIMEOUT_SECONDS = 30
ANONYMOUS_REQUEST_DELAY_SECONDS = 6

def fetch_cvss(cve_id: str) -> CvssInfo | None:
    api_key = os.getenv("NVD_API_KEY")
    headers = {"apiKey": api_key} if api_key else {}

    response = requests.get(
        NVD_CVE_API_URL, params={"cveId": cve_id}, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()

    if not api_key:
        time.sleep(ANONYMOUS_REQUEST_DELAY_SECONDS)

    vulnerabilities = payload.get("vulnerabilities", [])
    if not vulnerabilities:
        return None

    cve_data = vulnerabilities[0]["cve"]
    metrics = cve_data.get("metrics", {})
    affected = _extract_affected_configurations(cve_data)

    for key, label in (("cvssMetricV31", "3.1"), ("cvssMetricV30", "3.0"), ("cvssMetricV2", "2.0")):
        if metrics.get(key):
            data = metrics[key][0]["cvssData"]
            return CvssInfo(
                version=label,
                base_score=data["baseScore"],
                base_severity=data.get("baseSeverity", "UNKNOWN"),
                affected_configurations=affected,
            )

    return None

def _extract_affected_configurations(cve_data: dict) -> list[str]:
    results = []
    for config in cve_data.get("configurations", []):
        for node in config.get("nodes", []):
            for match in node.get("cpeMatch", []):
                if not match.get("vulnerable", False):
                    continue
                parts = match.get("criteria", "").split(":")
                if len(parts) < 6:
                    continue
                vendor, product, version = parts[3], parts[4], parts[5]

                version_range = ""
                if match.get("versionStartIncluding"):
                    version_range += f" {match['versionStartIncluding']} 이상"
                if match.get("versionEndExcluding"):
                    version_range += f" {match['versionEndExcluding']} 미만"
                elif match.get("versionEndIncluding"):
                    version_range += f" {match['versionEndIncluding']} 이하"

                version_text = version if version != "*" else "버전 정보 없음"
                results.append(f"{vendor}/{product} {version_text}{version_range}".strip())

    return list(dict.fromkeys(results))
