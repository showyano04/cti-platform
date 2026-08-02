from cti_platform.models import EnrichedVulnerability

CVSS_THRESHOLD = 7.0


def filter_by_cvss(candidates: list[EnrichedVulnerability]) -> list[EnrichedVulnerability]:
    """CVSS 7.0 이상인 항목만 남긴다."""
    return [v for v in candidates if v.cvss.base_score >= CVSS_THRESHOLD]