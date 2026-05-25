"""
Stage 1: 주제에서 영상 내레이션 스크립트 생성
"""
import os
import sys
import time
import json
import warnings
from pathlib import Path

# Python 3.9 관련 경고 숨기기 (작동엔 지장 없음)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=Warning, module="urllib3")

from google import genai
from dotenv import load_dotenv

# .env 로드
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 모델 — 본인 키로 사용 가능 확인됨
MODEL_NAME = "gemini-2.5-flash"


def generate_script(topic: str) -> str:
    """주제를 받아 60초 영상용 한국어 내레이션 스크립트 생성"""
    prompt = f"""다음 주제로 60초 분량의 한국어 영상 내레이션 스크립트를 작성해주세요.
- 4~6문장
- 도입 → 핵심 → 마무리 구조
- 자연스럽고 명확한 구어체

주제: {topic}

스크립트만 출력하고, 부가 설명은 포함하지 마세요."""

    start = time.time()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    elapsed = time.time() - start

    script = response.text.strip()

    # 시간 로깅
    log_path = Path("logs/timing.json")
    log_path.parent.mkdir(exist_ok=True)
    data = json.loads(log_path.read_text()) if log_path.exists() else {}
    data["01_script_generation"] = round(elapsed, 2)
    log_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"[01_script] {elapsed:.2f}초 소요 (model={MODEL_NAME})")

    # 결과 저장
    out_path = Path("outputs/script.txt")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(script, encoding="utf-8")

    return script


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI가 일자리에 미치는 영향"
    print(f"\n[입력] 주제: {topic}\n")
    result = generate_script(topic)
    print(f"\n[출력]\n{result}\n")
    print(f"저장 위치: outputs/script.txt")