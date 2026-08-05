from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# 💡 두 가지 프로바이더(Gemini, Claude)를 모두 가져옵니다.
from cve_platform.analyzers.gemini_provider import analyze_vulnerability as gemini_analyze
from cve_platform.analyzers.claude_provider import analyze_vulnerability as fallback_analyze

from cve_platform.collectors.cisa_kev import fetch_kev_catalog
from cve_platform.collectors.nvd_cvss import fetch_cvss
from cve_platform.generators.html_generator import generate_html
from cve_platform.generators.markdown_generator import generate_report
from cve_platform.models import EnrichedVulnerability
from cve_platform.processors.filter import filter_by_cvss
from cve_platform.processors.ranker import select_top
from cve_platform.publishers.github_pages import publish_to_github_pages

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
    print(f"CVSS 7.0 이상: {len(filtered)}건 → TOP5 분석 시작\n")

    for rank, vuln in enumerate(top5, start=1):
        print(f"{rank}. {vuln.kev.cve_id} 분석 중...")
        try:
            # 플랜 A: Gemini AI 심층 분석 시도
            vuln.analysis = gemini_analyze(vuln.kev, vuln.cvss)
        except Exception as e:
            # 플랜 B: 에러 발생 시(할당량 초과 등) 원본 데이터 기반 분석으로 우회
            print(f"  [Gemini 실패] {e} -> 플랜 B(팩트 데이터 추출) 가동!")
            try:
                vuln.analysis = fallback_analyze(vuln.kev, vuln.cvss)
            except Exception as fallback_e:
                print(f"  [플랜 B 완전 실패] {fallback_e}")

    report_date = date.today()
    markdown_content = generate_report(top5, report_date)
    html_content = generate_html(markdown_content, title=f"일간 주요 취약점(CVE) 분석 리포트 — {report_date.isoformat()}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    md_path = OUTPUT_DIR / f"report_{report_date.isoformat()}.md"
    md_path.write_text(markdown_content, encoding="utf-8")

    published_path = publish_to_github_pages(html_content, report_date)

    print(f"\n🎉 리포트 생성 및 배포 준비 완료!")
    print(f"👉 마크다운 원본: {md_path.absolute()}")
    print(f"👉 GitHub Pages 배포용 파일: {published_path.absolute()}")

if __name__ == "__main__":
    main()