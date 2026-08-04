import requests

from cti_platform.models import KevEntry

KEV_FEED_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
REQUEST_TIMEOUT_SECONDS = 30


def fetch_kev_catalog() -> list[KevEntry]:
    """CISA KEV 카탈로그 전체를 가져와 KevEntry 리스트로 반환한다."""
    response = requests.get(KEV_FEED_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    payload = response.json()
    return [KevEntry.model_validate(item) for item in payload["vulnerabilities"]]