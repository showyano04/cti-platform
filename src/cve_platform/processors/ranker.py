from cve_platform.models import EnrichedVulnerability


def select_top(candidates: list[EnrichedVulnerability], count: int = 5) -> list[EnrichedVulnerability]:
    """KEV 등재일 최신순, 동률이면 CVSS 높은 순으로 정렬해 상위 N개를 선정한다."""
    ranked = sorted(candidates, key=lambda v: (v.kev.date_added, v.cvss.base_score), reverse=True)
    return ranked[:count]
