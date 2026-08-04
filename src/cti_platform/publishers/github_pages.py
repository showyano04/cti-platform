from datetime import date
from pathlib import Path
from collections import defaultdict
import json

DOCS_DIR = Path("docs")
REPORTS_DIR = DOCS_DIR / "reports"
INDEX_FILE = DOCS_DIR / "index.html"

def publish_to_github_pages(html_content: str, report_date: date) -> Path:
    DOCS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    report_filename = f"report_{report_date.isoformat()}.html"
    report_path = REPORTS_DIR / report_filename
    report_path.write_text(html_content, encoding="utf-8")

    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    report_files = sorted(REPORTS_DIR.glob("*.html"), reverse=True)

    grouped_reports = defaultdict(list)
    monthly_counts = defaultdict(int)

    for index, file_path in enumerate(report_files):
        date_str = file_path.stem.replace("report_", "")
        try:
            parsed_date = date.fromisoformat(date_str)
            weekday_str = weekdays[parsed_date.weekday()]
            display_text = f"{date_str} ({weekday_str})"
            group_key = f"{parsed_date.year}년 {parsed_date.month}월"
            monthly_counts[group_key] += 1
        except ValueError:
            display_text = date_str
            group_key = "기타"

        latest_badge = '<span class="latest-badge">최신</span>' if index == 0 else ""
        
        card_html = f"""
            <a href="reports/{file_path.name}" class="report-link">
                <div class="report-card">
                    <span class="icon">🛡️</span>
                    <span class="title">일간 주요 취약점(CVE) 분석 리포트</span>
                    {latest_badge}
                    <span class="date">{display_text}</span>
                </div>
            </a>
        """
        grouped_reports[group_key].append(card_html)

    chart_labels = list(reversed(list(monthly_counts.keys())[:6]))
    chart_data = list(reversed(list(monthly_counts.values())[:6]))

    list_items_html = ""
    for month, cards in grouped_reports.items():
        list_items_html += f"""
            <div class="month-group">
                <h2 class="month-title">{month}</h2>
                <div class="report-list">
                    {"".join(cards)}
                </div>
            </div>
        """

    index_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CVE 보안 취약점 분석 모음</title>
    <!-- 💡 메인 페이지 SEO 최적화 -->
    <meta name="description" content="매일 업데이트되는 최신 보안 취약점(CVE) 동향 및 방어 가이드. 사이버 위협 인텔리전스를 무료로 구독하세요.">
    <meta name="keywords" content="CVE, 보안 취약점, 정보보안, CTI, 랜섬웨어, CISA KEV">
    <meta property="og:title" content="CVE 보안 취약점 분석 모음">
    <meta property="og:description" content="사이버 보안 담당자를 위한 일간 취약점 요약 리포트">
    
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        .container {{ max-width: 850px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.2rem; color: #1e293b; margin-bottom: 10px; font-weight: 800; }}
        .header p {{ color: #64748b; font-size: 1.1rem; }}
        
        /* 💡 구독 폼 CSS */
        .subscribe-box {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #bfdbfe; border-radius: 12px;
            padding: 25px 30px; margin-bottom: 40px; text-align: center;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
        }}
        .subscribe-box h3 {{ margin: 0 0 10px 0; color: #1e40af; font-size: 1.3rem; }}
        .subscribe-box p {{ margin: 0 0 20px 0; color: #3b82f6; font-size: 0.95rem; }}
        .subscribe-form {{ display: flex; gap: 10px; justify-content: center; max-width: 500px; margin: 0 auto; }}
        .subscribe-form input {{
            flex-grow: 1; padding: 12px 15px; border: 1px solid #cbd5e1;
            border-radius: 8px; font-size: 1rem; outline: none;
        }}
        .subscribe-form input:focus {{ border-color: var(--primary); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); }}
        .subscribe-form button {{
            background-color: var(--primary); color: white; border: none;
            padding: 12px 25px; border-radius: 8px; font-size: 1rem;
            font-weight: 600; cursor: pointer; transition: background-color 0.2s;
        }}
        .subscribe-form button:hover {{ background-color: #2563eb; }}

        .dashboard {{
            background: var(--card-bg); border: 1px solid var(--border);
            border-radius: 12px; padding: 25px; margin-bottom: 40px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .dashboard-title {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 20px; color: #1e293b; }}
        
        .month-group {{ margin-bottom: 40px; }}
        .month-title {{ 
            font-size: 1.3rem; color: #334155; font-weight: 800;
            border-bottom: 2px solid var(--border); 
            padding-bottom: 10px; margin-bottom: 15px; 
        }}
        
        .report-list {{ display: flex; flex-direction: column; gap: 15px; }}
        .report-link {{ text-decoration: none; color: inherit; }}
        .report-card {{
            display: flex; align-items: center; justify-content: space-between;
            background: var(--card-bg); padding: 20px 25px;
            border: 1px solid var(--border); border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: all 0.2s ease-in-out;
        }}
        .report-card:hover {{
            transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            border-color: var(--primary); background-color: var(--hover-bg);
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
        
        @media (max-width: 600px) {{
            .subscribe-form {{ flex-direction: column; }}
            .subscribe-form button {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ CVE 보안 취약점 분석 모음</h1> 
            <p>CISA KEV 및 NVD 데이터를 기반으로 자동 분석된 일간 리포트 모음입니다.</p>
        </div>
        
        <!-- 💡 수익화를 위한 뉴스레터 구독 폼 -->
        <div class="subscribe-box">
            <h3>💌 보안 위협 트렌드, 놓치지 마세요</h3>
            <p>가장 치명적인 취약점 분석과 방어 가이드를 매일 아침 이메일로 무료 배달해 드립니다.</p>
<!-- 💡 Mailchimp 등 실제 서비스 연동을 위한 표준 폼 형식으로 변경 -->
            <form class="subscribe-form" action="여기에_메일서비스_구독URL_입력" method="POST" target="_blank">
                <input type="email" name="EMAIL" placeholder="이메일 주소를 입력하세요" required>
                <button type="submit">구독하기</button>
            </form>
        </div>

        <div class="dashboard">
            <div class="dashboard-title">📊 월별 취약점 리포트 발행 추이</div>
            <canvas id="trendChart" height="80"></canvas>
        </div>

        <div class="archive">
            {list_items_html}
        </div>
    </div>

    <script>
        const ctx = document.getElementById('trendChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(chart_labels)},
                datasets: [{{
                    label: '발행된 리포트 수',
                    data: {json.dumps(chart_data)},
                    backgroundColor: '#3b82f6',
                    borderRadius: 6,
                    maxBarThickness: 50
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
            }}
        }});
    </script>
</body>
</html>"""

    INDEX_FILE.write_text(index_html, encoding="utf-8")
    return report_path