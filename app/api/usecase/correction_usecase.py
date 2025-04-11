from tsidpy import TSID

from app.common.utils.logger import get_logger
from app.infrastructure.clients.llm.alibaba.qwen_client import QwenTurboClient
from app.infrastructure.clients.llm.llm_client import LlmClient
from app.infrastructure.clients.storage.audio_storage_client import AudioStorageClient
from app.infrastructure.clients.storage.local.local_audio_storage_client import LocalAudioStorageClient
from app.infrastructure.clients.stt.naver.naver_stt_client import NaverClovaSpeechRecognizer
from app.infrastructure.clients.stt.speech_recognizer import SpeechRecognizer
from app.api.dto.correct_dto import CorrectionResponse
from app.api.mapper.correction_mapper import to_correction_response

logger = get_logger(__name__)

async def correct(
    command: bytes,
    speech_recognizer: SpeechRecognizer = NaverClovaSpeechRecognizer(),
    llm_client: LlmClient = QwenTurboClient(),
    audio_storage_client: AudioStorageClient = LocalAudioStorageClient()
) -> CorrectionResponse:
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
        text = await speech_recognizer.recognize(audio_data=command.original)
        correction_result = await llm_client.correct_text(text)

        return to_correction_response(
                id=TSID.create().number, 
                data=correction_result
            )
    except Exception as e:
        logger.error(f"Error in process_correction_request: {e}")
        raise e
