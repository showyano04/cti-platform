from datetime import date
from pathlib import Path
from dotenv import load_dotenv

from cti_platform.analyzers.gemini_provider import analyze_vulnerability
from cti_platform.collectors.cisa_kev import fetch_kev_catalog
from cti_platform.collectors.nvd_cvss import fetch_cvss
from cti_platform.generators.html_generator import generate_html
from cti_platform.generators.markdown_generator import generate_report
from cti_platform.models import EnrichedVulnerability
from cti_platform.processors.filter import filter_by_cvss
from cti_platform.processors.ranker import select_top
from cti_platform.publishers.github_pages import publish_to_github_pages

load_dotenv()

RECENT_ENTRY_COUNT = 20
OUTPUT_DIR = Path("content")

def main() -> None:
    entries = fetch_kev_catalog()
    print(f"KEV 카탈로그에서 총 {len(entries)}건의 취약점을 가져왔습니다.")

    recent = sorted(entries, key=lambda e: e.date_added, reverse=True)[:RECENT_ENTRY_COUNT]
    enriched: list[EnrichedVulnerability] = []
    
    print("CVSS 조회를 시작합니다...")
    for entry in recent:
        cvss = fetch_cvss(entry.cve_id)
        if cvss is not None:
            enriched.append(EnrichedVulnerability(kev=entry, cvss=cvss))

    filtered = filter_by_cvss(enriched)
    top5 = select_top(filtered, count=5)
    print(f"CVSS 7.0 이상: {len(filtered)}건 → TOP5 분석 시작 (Gemini AI)\n")

    for rank, vuln in enumerate(top5, start=1):
        print(f"{rank}. {vuln.kev.cve_id} 분석 중...")
        try:
            vuln.analysis = analyze_vulnerability(vuln.kev, vuln.cvss)
        except Exception as e:
            print(f"  [분석 실패] {e}")

    analyzed_count = sum(1 for v in top5 if v.analysis is not None)
    if analyzed_count == 0:
        raise RuntimeError("모든 취약점 분석이 실패했습니다. API 키/시크릿 설정을 확인하세요.")

    report_date = date.today()
    markdown_content = generate_report(top5, report_date)
    html_content = generate_html(markdown_content, title=f"주간 CTI 리포트 — {report_date.isoformat()}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    md_path = OUTPUT_DIR / f"report_{report_date.isoformat()}.md"
    md_path.write_text(markdown_content, encoding="utf-8")

    published_path = publish_to_github_pages(html_content, report_date)

    print(f"\n🎉 리포트 생성 및 배포 준비 완료!")
    print(f"👉 마크다운 원본: {md_path.absolute()}")
    print(f"👉 GitHub Pages 배포용 파일: {published_path.absolute()}")

if __name__ == "__main__":
    main()