import re

def extract_references(notes: str) -> list[str]:
    """KEV notes 필드에서 URL만 추출한다 (LLM이 아닌 코드가 직접 처리 — 환각 방지)."""
    return re.findall(r"https?://\S+", notes)
