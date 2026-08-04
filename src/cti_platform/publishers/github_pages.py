from datetime import date
from pathlib import Path
from collections import defaultdict
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

DOCS_DIR = Path("docs")
REPORTS_DIR = DOCS_DIR / "reports"
INDEX_FILE = DOCS_DIR / "index.html"

def send_cve_report_via_gmail(html_content, report_date, subscriber_list):
    """구글(Gmail) 서버를 통해 구독자에게 CVE 리포트를 자동 발송하는 함수"""
    
    # 1. 깃허브 시크릿에서 민감한 구글 로그인 정보 가져오기
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD') # 1단계에서 발급받은 앱 비밀번호

    if not gmail_user or not gmail_app_password:
        print("🛑 구글 로그인 정보가 깃허브 시크릿에 설정되지 않았습니다. 메일 발송을 스킵합니다.")
        return

    print(f"📧 총 {len(subscriber_list)}명의 구독자에게 지메일로 리포트를 발송합니다...")

    # 2. 메일 제목 설정 (예: [확인] 2026-08-04 CVE 보안 취약점 일간 분석 리포트)
    subject = f"[{report_date.isoformat()}] CVE 보안 취약점 일간 분석 리포트"

    # 3. 구글 SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    port = 465  # SSL 용 포트

    # 4. 메일 발송 반복문 실행
    for subscriber_email in subscriber_list:
        try:
            # MIME 프로토콜로 메일 구성 (HTML + 텍스트)
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"CVE 보안 리포트 <{gmail_user}>"
            
            # (중요!) 구독자의 이메일은 Bcc(숨은참조)에 넣어 개인정보를 보호합니다.
            message["Bcc"] = subscriber_email

            # 이메일 본문 (HTML 버전)
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # 보안 컨텍스트 생성 및 SSL 보안 연결 시도
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(gmail_user, gmail_app_password)
                # 메일 발송 실행
                server.sendmail(gmail_user, subscriber_email, message.as_string())
                print(f"  ✅ {subscriber_email} 발송 성공!")

        except Exception as e:
            print(f"  🛑 {subscriber_email} 발송 실패: {e}")

    print("🎉 모든 구독자에게 메일 발송이 완료되었습니다!")

def publish_to_github_pages(html_content: str, report_date: date) -> Path:
    """웹사이트 업데이트 및 메일 자동 발송을 동시에 수행하는 메인 함수"""
    
    # [기존 코드 - 웹사이트 생성 및 업데이트 부분 (그대로 유지)]
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
    <!-- [기존 HTML 코드 그대로 유지...] -->
</head>
<body>
    <!-- [기존 HTML 코드 그대로 유지...] -->
</body>
</html>"""

    INDEX_FILE.write_text(index_html, encoding="utf-8")
    # [기존 코드 끝]

    # --- ✨ 자동화의 핵심! 풀버전 코드에서 새롭게 추가된 부분 ✨ ---

    # 1. 스티비에서 수집된 구독자 목록 가져오기 (테스트를 위해 일단 대표님의 지메일만 등록)
    # TODO: 추후 구독자가 늘어나면 스티비 주소록을 이 environment variable에 업데이트해 주셔야 합니다.
    subscribers = os.environ.get('SUBSCRIBER_EMAILS', '').split(',')
    
    # 빈 값 제거 (예: ',,,' 등)
    subscribers = [email.strip() for email in subscribers if email.strip()]

    # 2. 지메일 서버를 통해 단체 메일 발송 실행!
    if subscribers:
        send_cve_report_via_gmail(html_content, report_date, subscribers)
    else:
        print("🛑 등록된 구독자가 없습니다. 메일 발송을 스킵합니다.")

    return report_path