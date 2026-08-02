import markdown as md

def generate_html(markdown_content: str, title: str) -> str:
    """Markdown 콘텐츠를 HTML 문서로 변환한다."""
    body = md.markdown(markdown_content, extensions=["extra"])
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 40px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        strong {{ color: #e74c3c; }}
    </style>
</head>
<body>
{body}
</body>
</html>"""