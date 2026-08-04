from datetime import date

from cti_platform.models import EnrichedVulnerability
from cti_platform.utils import extract_references

_SEVERITY_CLASS = {
    "CRITICAL": "sev-critical",
    "HIGH": "sev-high",
    "MEDIUM": "sev-medium",
    "LOW": "sev-low",
}


def _severity_badge(severity: str) -> str:
    css_class = _SEVERITY_CLASS.get(severity, "sev-unknown")
    return f'<span class="severity-badge {css_class}">{severity}</span>'


def _ransomware_badge(known_ransomware_use: str) -> str:
    if known_ransomware_use == "Known":
        return ' <span class="ransomware-badge">\U0001F525 \uB79C\uC12C\uC6E8\uC5B4 \uC5F0\uAD00</span>'
    return ""


def generate_report(vulnerabilities: list[EnrichedVulnerability], report_date: date) -> str:
    """TOP5 취약점으로 주간 Markdown 리포트를 생성한다."""
    lines = [f"# 주간 주요 취약점(CVE) 분석 리포트 — {report_date.isoformat()}", ""]

    for rank, vuln in enumerate(vulnerabilities, start=1):
        if not vuln.analysis:
            continue

        analysis = vuln.analysis
        references = extract_references(vuln.kev.notes)
        lines += [
            f"## {rank}. {vuln.kev.cve_id} — {vuln.kev.vulnerability_name}",
            "",
            f"- **CVSS**: {vuln.cvss.base_score} {_severity_badge(vuln.cvss.base_severity)}",
            f"- **KEV 등재**: 예 (등재일 {vuln.kev.date_added}, 패치 기한 {vuln.kev.due_date})",
            f"- **영향 제품**: {vuln.kev.vendor_project} {vuln.kev.product}",
            f"- **영향 버전(NVD 기준)**: {analysis.affected_versions}",
            f"- **랜섬웨어 연관**: {vuln.kev.known_ransomware_use}{_ransomware_badge(vuln.kev.known_ransomware_use)}",
            "",
            f"**개요**: {analysis.summary}",
            "",
            f"**공격 영향**: {analysis.attack_impact}",
            "",
            f"**패치 우선순위**: {analysis.patch_priority}",
            "",
            f"**공식 패치·완화조치(CISA 권고)**: {vuln.kev.required_action}",
            "",
            "**운영자 확인 사항**:",
        ]
        lines += [f"- {item}" for item in analysis.operator_checklist]
        lines.append("")
        lines.append("**참고 자료**:")
        if references:
            lines += [f"- [{ref}]({ref})" for ref in references]
        else:
            lines.append("- 제공된 데이터에 없음")
        lines.append("")

    lines += _build_weekly_summary(vulnerabilities)
    return "\n".join(lines)


def _build_weekly_summary(vulnerabilities: list[EnrichedVulnerability]) -> list[str]:
    ransomware_count = sum(1 for v in vulnerabilities if v.kev.known_ransomware_use == "Known")
    vendors = sorted({v.kev.vendor_project for v in vulnerabilities})
    avg_cvss = sum(v.cvss.base_score for v in vulnerabilities) / len(vulnerabilities)
    all_items = [item for v in vulnerabilities if v.analysis for item in v.analysis.operator_checklist]
    deduped_checklist = list(dict.fromkeys(all_items))

    return [
        "## 이번 주 보안 트렌드",
        "",
        f"- 평균 CVSS: {avg_cvss:.1f}",
        f"- 랜섬웨어 연관: {ransomware_count}건 / {len(vulnerabilities)}건",
        f"- 영향받은 벤더: {', '.join(vendors)}",
        "",
        "## 운영자 체크리스트 (종합)",
        "",
        *[f"- {item}" for item in deduped_checklist],
        "",
        "## 이번 주 핵심 요약",
        "",
        f"이번 주는 {', '.join(v.kev.cve_id for v in vulnerabilities)} 총 {len(vulnerabilities)}건의 "
        f"KEV 등재 취약점을 다뤘습니다. 평균 CVSS {avg_cvss:.1f}, 랜섬웨어 연관 {ransomware_count}건입니다.",
        "",
    ]