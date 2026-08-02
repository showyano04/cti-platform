from dotenv import load_dotenv

from cti_platform.collectors.cisa_kev import fetch_kev_catalog
from cti_platform.collectors.nvd_cvss import fetch_cvss
from cti_platform.models import EnrichedVulnerability
from cti_platform.processors.filter import filter_by_cvss
from cti_platform.processors.ranker import select_top

load_dotenv()

RECENT_ENTRY_COUNT = 20


def main() -> None:
    entries = fetch_kev_catalog()
    print(f"KEV 카탈로그에서 총 {len(entries)}건의 취약점을 가져왔습니다.")

    recent = sorted(entries, key=lambda e: e.date_added, reverse=True)[:RECENT_ENTRY_COUNT]
    print(f"최근 등재된 {len(recent)}건에 CVSS를 조회합니다 (시간이 좀 걸릴 수 있습니다)...")

    enriched: list[EnrichedVulnerability] = []
    for entry in recent:
        cvss = fetch_cvss(entry.cve_id)
        if cvss is not None:
            enriched.append(EnrichedVulnerability(kev=entry, cvss=cvss))

    filtered = filter_by_cvss(enriched)
    print(f"CVSS 7.0 이상: {len(filtered)}건")

    top5 = select_top(filtered, count=5)
    print("이번 주 TOP5:")
    for rank, vuln in enumerate(top5, start=1):
        print(
            f"  {rank}. {vuln.kev.cve_id} — CVSS {vuln.cvss.base_score} ({vuln.cvss.base_severity}) "
            f"— {vuln.kev.vendor_project} {vuln.kev.product} — 등재일 {vuln.kev.date_added}"
        )


if __name__ == "__main__":
    main()