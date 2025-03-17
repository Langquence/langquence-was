from typing import List

from pydantic import BaseModel

from app.common.utils.logger import get_logger
from app.domain.services.pattern_matching import validate_correction
from app.infrastructure.clients.llm.alibaba.qwen_client import QwenTurboClient
from app.infrastructure.clients.llm.llm_client import LlmClient
from app.infrastructure.clients.stt.naver.naver_stt_client import NaverClovaSpeechRecognizer
from app.infrastructure.clients.stt.speech_recognizer import SpeechRecognizer

logger = get_logger(__name__)


class CorrectionCommand(BaseModel):
    original: bytes


class CorrectionResult(BaseModel):
    original: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []


async def process_correction_request(
        command: CorrectionCommand,
        speech_recognizer: SpeechRecognizer = NaverClovaSpeechRecognizer(),
        llm_client: LlmClient = QwenTurboClient()
):
    try:
        # 1. STT 결과 추출
        text = await speech_recognizer.recognize(audio_data=command.original)

        # 1. 텍스트 교정 (API 호출)
        correction_result = await llm_client.correct_text(text)

        # 2. 패턴 매칭 검증
        validated_result = await validate_correction(correction_result)

        return CorrectionResult(
            original=validated_result.original,
            needs_correction=validated_result.needs_correction,
            corrected=validated_result.corrected,
            explanation=validated_result.explanation,
            alternatives=validated_result.alternatives
        )
    except Exception as e:
        logger.error(f"process_correction_request 오류: {e}")

        raise e
