$content = @'
from datetime import date
from pathlib import Path

DOCS_DIR = Path("docs")
REPORTS_DIR = DOCS_DIR / "reports"
INDEX_FILE = DOCS_DIR / "index.html"

def publish_to_github_pages(html_content: str, report_date: date) -> Path:
    DOCS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    report_filename = f"report_{report_date.isoformat()}.html"
    report_path = REPORTS_DIR / report_filename
    report_path.write_text(html_content, encoding="utf-8")

    weekdays = ["\uC6D4", "\uD654", "\uC218", "\uBAA9", "\uAE08", "\uD1A0", "\uC77C"]

    report_files = sorted(REPORTS_DIR.glob("*.html"), reverse=True)

    list_items = ""
    for index, file_path in enumerate(report_files):
        date_str = file_path.stem.replace("report_", "")
        try:
            parsed_date = date.fromisoformat(date_str)
            weekday_str = weekdays[parsed_date.weekday()]
            display_text = f"{date_str} ({weekday_str})"
        except ValueError:
            display_text = date_str

        latest_badge = '<span class="latest-badge">\uCD5C\uC2E0</span>' if index == 0 else ""

        list_items += f"""
            <a href="reports/{file_path.name}" class="report-link">
                <div class="report-card">
                    <span class="icon">\U0001F6E1\uFE0F</span>
                    <span class="title">주간 주요 취약점(CVE) 분석 리포트</span>
                    {latest_badge}
                    <span class="date">{display_text}</span>
                </div>
            </a>
        """

    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주간 주요 취약점(CVE) 분석 리포트 아카이브</title>
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <style>
        :root {{
            --bg-color: #f8fafc;
            --text-color: #0f172a;
            --primary: #3b82f6;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --hover-bg: #eff6ff;
        }}
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0; padding: 40px 20px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 50px; }}
        .header h1 {{ font-size: 2.2rem; color: #1e293b; margin-bottom: 10px; }}
        .header p {{ color: #64748b; font-size: 1.1rem; }}
        .report-list {{ display: flex; flex-direction: column; gap: 15px; }}
        .report-link {{ text-decoration: none; color: inherit; }}

        .report-card {{
            display: flex; align-items: center; justify-content: space-between;
            background: var(--card-bg);
            padding: 20px 25px;
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease-in-out;
        }}
        .report-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            border-color: var(--primary);
            background-color: var(--hover-bg);
        }}
        .report-card .icon {{ font-size: 1.5rem; margin-right: 15px; }}
        .report-card .title {{ flex-grow: 1; font-weight: 600; font-size: 1.1rem; }}
        .report-card .date {{
            color: #64748b; font-size: 0.95rem; font-weight: 600;
            background: #f1f5f9; padding: 6px 14px; border-radius: 20px;
        }}
        .latest-badge {{
            color: #fff; font-size: 0.8rem; font-weight: 700;
            background: var(--primary); padding: 4px 12px; border-radius: 20px;
            margin-right: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>\U0001F3AF 주요 취약점(CVE) 분석 아카이브</h1>
            <p>CISA KEV 및 NVD 데이터를 기반으로 자동 분석된 주간 리포트 모음입니다.</p>
        </div>
        <div class="report-list">
            {list_items}
        </div>
    </div>
</body>
</html>"""

    INDEX_FILE.write_text(index_html, encoding="utf-8")
    return report_path
'@
[System.IO.File]::WriteAllText("$PWD\src\cti_platform\publishers\github_pages.py", $content, [System.Text.UTF8Encoding]::new($false))