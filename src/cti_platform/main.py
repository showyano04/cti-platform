from cti_platform.collectors.cisa_kev import fetch_kev_catalog


def main() -> None:
    entries = fetch_kev_catalog()
    print(f"KEV 카탈로그에서 총 {len(entries)}건의 취약점을 가져왔습니다.")

    recent = sorted(entries, key=lambda e: e.date_added, reverse=True)[:5]
    print("최근 등재된 5건:")
    for entry in recent:
        print(f"  - {entry.cve_id} ({entry.date_added}) — {entry.vendor_project} {entry.product}")


if __name__ == "__main__":
    main()