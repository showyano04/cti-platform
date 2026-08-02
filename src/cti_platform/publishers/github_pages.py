from datetime import date
from pathlib import Path

DOCS_DIR = Path("docs")
REPORTS_DIR = DOCS_DIR / "reports"

def publish_to_github_pages(html_content: str, report_date: date) -> Path:
    """리포트 HTML을 docs/ 폴더에 기록하고 인덱스 페이지를 갱신한다."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report_path = REPORTS_DIR / f"report_{report_date.isoformat()}.html"
    report_path.write_text(html_content, encoding="utf-8")

    _rebuild_index()
    return report_path

def _rebuild_index() -> None:
    report_files = sorted(REPORTS_DIR.glob("report_*.html"), reverse=True)
    links = "\n".join(
        f'<li><a href="reports/{f.name}">{f.stem.replace("report_", "")}</a></li>'
        for f in report_files
    )
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>주간 CTI 리포트</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; }}
        h1 {{ border-bottom: 2px solid #2c3e50; padding-bottom: 10px; color: #2c3e50; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; }}
        a {{ text-decoration: none; color: #3498db; font-size: 1.1em; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🎯 주간 CTI 리포트 아카이브</h1>
    <ul>{links}</ul>
</body>
</html>"""
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")