import markdown as md

def generate_html(markdown_content: str, title: str) -> str:
    body = md.markdown(markdown_content, extensions=["extra"])
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- 💡 SEO 및 소셜 미디어 공유 최적화(OpenGraph) -->
    <meta name="description" content="CISA KEV 및 NVD 기반 최신 보안 취약점 심층 분석 리포트">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="가장 치명적인 보안 취약점 정보와 운영자 방어 가이드를 확인하세요.">
    <meta property="og:type" content="article">
    
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <style>
        :root {{
            --bg-color: #f3f4f6;
            --text-color: #1f2937;
            --card-bg: #ffffff;
            --primary: #2563eb;
            --accent: #dc2626;
            --border: #e5e7eb;
        }}
        body {{
            font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.7;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 850px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 40px 50px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        h1, h2, h3 {{ color: #111827; }}
        h1 {{ font-size: 1.8rem; border-bottom: 2px solid var(--primary); padding-bottom: 10px; margin-bottom: 30px; }}
        h2 {{ font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-top: 40px; }}
        h3 {{ font-size: 1.25rem; color: var(--primary); margin-top: 30px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 10px; }}
        strong {{ color: var(--accent); font-weight: 600; }}
        a {{ color: var(--primary); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
        blockquote {{ border-left: 4px solid var(--primary); margin: 0; padding-left: 16px; color: #4b5563; background: #f9fafb; padding: 10px 16px; border-radius: 0 8px 8px 0; }}
        .back-link {{ display: inline-block; margin-bottom: 20px; font-weight: 600; color: #6b7280; }}
        .back-link:hover {{ color: var(--primary); }}
        .severity-badge {{
            display: inline-block; padding: 2px 12px; border-radius: 999px;
            font-size: 0.78rem; font-weight: 700; color: #fff;
            vertical-align: middle; letter-spacing: 0.02em;
        }}
        .sev-critical {{ background: #dc2626; }}
        .sev-high {{ background: #ea580c; }}
        .sev-medium {{ background: #d97706; }}
        .sev-low {{ background: #65a30d; }}
        .sev-unknown {{ background: #6b7280; }}
        .ransomware-badge {{
            display: inline-block; padding: 2px 12px; border-radius: 999px;
            font-size: 0.78rem; font-weight: 700; color: #991b1b;
            background: #fee2e2; margin-left: 6px; vertical-align: middle;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← 아카이브 목록으로 돌아가기</a>
        {body}
    </div>
</body>
</html>"""
