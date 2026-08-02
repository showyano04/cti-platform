from dotenv import load_dotenv

from cti_platform.collectors.cisa_kev import fetch_kev_catalog
from cti_platform.collectors.nvd_cvss import fetch_cvss

load_dotenv()

RECENT_ENTRY_COUNT = 20


def main() -> None:
    entries = fetch_kev_catalog()
    print(f"KEV 카탈로그에서 총 {len(entries)}건의 취약점을 가져왔습니다.")

    recent = sorted(entries, key=lambda e: e.date_added, reverse=True)[:RECENT_ENTRY_COUNT]
    print(f"최근 등재된 {len(recent)}건에 CVSS를 조회합니다 (시간이 좀 걸릴 수 있습니다)...")

    for entry in recent:
        cvss = fetch_cvss(entry.cve_id)
        cvss_text = f"CVSS {cvss.base_score} ({cvss.base_severity})" if cvss else "CVSS 미정(분석 대기 중)"
        print(f"  - {entry.cve_id} ({entry.date_added}) — {entry.vendor_project} {entry.product} — {cvss_text}")


if __name__ == "__main__":
    main()