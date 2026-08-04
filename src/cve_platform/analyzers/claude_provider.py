from cti_platform.models import CvssInfo, KevEntry, VulnerabilityAnalysis

def analyze_vulnerability(kev: KevEntry, cvss: CvssInfo) -> VulnerabilityAnalysis:
    """
    AI API 결제를 생략하고, 수집된 원본(팩트) 데이터만 정직하게 추출하여 리포트 포맷으로 반환합니다.
    (거짓말/가짜 데이터 0%)
    """
    return VulnerabilityAnalysis(
        summary=f"[원본 요약] {kev.short_description}",
        attack_impact="상세 공격 영향은 원본 데이터에 명시되지 않음",
        patch_priority=f"CVSS {cvss.base_score} ({cvss.base_severity}) / CISA 권고: {kev.required_action}",
        operator_checklist=[
            f"영향받는 제품 확인: {kev.vendor_project} {kev.product}",
            f"벤더사 패치 적용 기한 준수: {kev.due_date} 까지"
        ]
    )