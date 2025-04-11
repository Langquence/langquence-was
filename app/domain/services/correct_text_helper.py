from typing import List

from pydantic import BaseModel
from tsidpy import TSID

from app.common.utils.logger import get_logger
from app.domain.services.pattern_matching import validate_correction
from app.infrastructure.clients.llm.alibaba.qwen_client import QwenTurboClient
from app.infrastructure.clients.llm.llm_client import LlmClient
from app.infrastructure.clients.storage.audio_storage_client import AudioStorageClient
from app.infrastructure.clients.storage.local.local_audio_storage_client import LocalAudioStorageClient
from app.infrastructure.clients.stt.naver.naver_stt_client import NaverClovaSpeechRecognizer
from app.infrastructure.clients.stt.speech_recognizer import SpeechRecognizer

logger = get_logger(__name__)


class CorrectionCommand(BaseModel):
    original: bytes


class CorrectionResult(BaseModel):
    id: int
    original: str
    boundary_corrected: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []


async def process_correction_request(
        command: CorrectionCommand,
        speech_recognizer: SpeechRecognizer = NaverClovaSpeechRecognizer(),
        llm_client: LlmClient = QwenTurboClient(),
        audio_storage_client: AudioStorageClient = LocalAudioStorageClient()
) -> CorrectionResult:
    """
    Processes a correction request by performing speech-to-text, text correction, and validation.

    Args:
        command (CorrectionCommand): The command containing the original audio data.
        speech_recognizer (SpeechRecognizer): The speech recognizer client.
        llm_client (LlmClient): The language model client for text correction.
        audio_storage_client (AudioStorageClient): The client for storing audio data.

    Returns:
        CorrectionResult: The result of the correction process.

    Raises:
        Exception: If any error occurs during the process.
    """
    saved_url = await audio_storage_client.save_audio(command.original, "wav")
    logger.info(f"Saved audio file path: {saved_url}")

    try:
        # 1. STT 결과 추출
        text = await speech_recognizer.recognize(audio_data=command.original)

        # 2. 텍스트 교정 (API 호출)
        correction_result = await llm_client.correct_text(text)

        # 3. 패턴 매칭 검증
        validated_result = await validate_correction(correction_result)
        
        # 4. DB 저장 (추후 수정)
        # correction_entity = correction_repository.save()

        return CorrectionResult(
            id=TSID.create().number,
            original=validated_result.original,
            boundary_corrected=validated_result.boundary_corrected,
            needs_correction=validated_result.needs_correction,
            corrected=validated_result.corrected,
            explanation=validated_result.explanation,
            alternatives=validated_result.alternatives
        )
    except Exception as e:
        logger.error(f"Error in process_correction_request: {e}")
        raise e
