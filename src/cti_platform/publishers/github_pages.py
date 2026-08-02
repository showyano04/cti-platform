from datetime import date
from pathlib import Path

DOCS_DIR = Path("docs")
REPORTS_DIR = DOCS_DIR / "reports"
INDEX_FILE = DOCS_DIR / "index.html"

def publish_to_github_pages(html_content: str, report_date: date) -> Path:
    DOCS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    # 개별 리포트 저장
    report_filename = f"report_{report_date.isoformat()}.html"
    report_path = REPORTS_DIR / report_filename
    report_path.write_text(html_content, encoding="utf-8")

    # 요일 매핑 배열
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    # reports 폴더 내의 모든 html 파일을 읽어서 목록 생성 (최신순 정렬)
    report_files = sorted(REPORTS_DIR.glob("*.html"), reverse=True)
    
    list_items = ""
    for file_path in report_files:
        # 파일명에서 날짜 추출 (report_2026-08-03.html -> 2026-08-03)
        date_str = file_path.stem.replace("report_", "")
        try:
            # 추출한 문자열을 실제 날짜로 변환하여 요일 계산
            parsed_date = date.fromisoformat(date_str)
            weekday_str = weekdays[parsed_date.weekday()]
            display_text = f"{date_str} ({weekday_str})"
        except ValueError:
            display_text = date_str # 날짜 형식이 아니면 파일명 그대로 출력

        # 세련된 카드 형태의 리스트 아이템 생성
        list_items += f"""
            <a href="reports/{file_path.name}" class="report-link">
                <div class="report-card">
                    <span class="icon">🛡️</span>
                    <span class="title">주간 주요 취약점(CVE) 분석 리포트</span>
                    <span class="date">{display_text}</span>
                </div>
            </a>
        """

    # 메인 페이지(index.html) CSS 템플릿
    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주간 주요 취약점(CVE) 분석 리포트 아카이브</title>
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 주요 취약점(CVE) 분석 아카이브</h1>
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