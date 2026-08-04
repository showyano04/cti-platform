from pathlib import Path
from google import genai
from google.genai import types
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential
from cti_platform.models import CvssInfo, KevEntry, VulnerabilityAnalysis

PROMPT_PATH = Path.cwd() / "prompt.md"
# API 목록 확인을 통해 검증된 최신 표준 모델명 사용
MODEL_NAME = "gemini-2.5-flash"

def _is_retryable(exception: BaseException) -> bool:
    """일일 quota 소진(RESOURCE_EXHAUSTED)은 기다려도 풀리지 않으므로 재시도하지 않는다."""
    return "RESOURCE_EXHAUSTED" not in str(exception)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=20),
    retry=retry_if_exception(_is_retryable),
    reraise=True,
)
def analyze_vulnerability(kev: KevEntry, cvss: CvssInfo) -> VulnerabilityAnalysis:
    """Gemini 무료 티어로 취약점을 분석한다."""
    client = genai.Client()
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    affected_text = (
        "; ".join(cvss.affected_configurations)
        if cvss.affected_configurations
        else "제공된 데이터에 상세 버전 정보 없음"
    )

    user_content = (
        f"CVE ID: {kev.cve_id}\n"
        f"제품: {kev.vendor_project} {kev.product}\n"
        f"취약점명: {kev.vulnerability_name}\n"
        f"CISA 설명: {kev.short_description}\n"
        f"CVSS: {cvss.base_score} ({cvss.base_severity}, v{cvss.version})\n"
        f"영향받는 제품/버전 (NVD CPE 데이터): {affected_text}\n"
        f"랜섬웨어 연관: {kev.known_ransomware_use}\n"
        f"CISA 권고 조치: {kev.required_action}\n"
        f"패치 기한: {kev.due_date}\n"
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_content,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=VulnerabilityAnalysis,
        ),
    )
    return VulnerabilityAnalysis.model_validate_json(response.text)