import os
from datetime import datetime

import scipy.io.wavfile as wavfile

from app.common.utils.logger import get_logger
from app.common.utils.wav_util import diagnose_wav_bytes, extract_wav_info
from app.infrastructure.clients.storage.audio_storage_client import AudioStorageClient

logger = get_logger(__name__)


class LocalAudioStorageClient(AudioStorageClient):
    """로컬 파일 시스템을 이용한 오디오 저장"""

    async def save_audio(self, audio_data: bytes, extension: str) -> str:
        """
        WAV 데이터를 파일로 저장합니다.
        현재는 WAV 파일만 지원합니다.
        """
        if extension != "wav":
            logger.warning(f"Unsupported audio extension: {extension}")
            return ""

        file_path = self._create_storage_dir()

        # WAV 헤더 진단
        header_info = diagnose_wav_bytes(audio_data)
        if "error" in header_info:
            logger.warning(f"WAV header diagnosis failed: {header_info['error']}")
        else:
            logger.info(f"WAV header info: {header_info}")

        saved_path = None
        # 방법 1: scipy로 처리 시도
        try:
            sampling_rate, data = extract_wav_info(audio_data)
            if sampling_rate is not None and data is not None:
                wavfile.write(file_path, sampling_rate, data)
                logger.info(f"Successfully saved WAV using scipy: {sampling_rate}Hz, {data.shape} samples")
                saved_path = file_path
        except Exception as e:
            logger.warning(f"Failed to process with scipy: {str(e)}")

        # 방법 1이 실패하면 방법 2: 직접 바이트 저장
        if saved_path is None:
            try:
                with open(file_path, 'wb') as file:
                    file.write(audio_data)
                logger.info(f"Saved raw bytes to {file_path}, size: {len(audio_data)} bytes")
                saved_path = file_path
            except Exception as e:
                logger.error(f"Failed to save raw bytes: {str(e)}")
                return ""

        return saved_path

    @staticmethod
    def _create_storage_dir() -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_dir = "debug_audio"
        os.makedirs(debug_dir, exist_ok=True)

        return os.path.join(debug_dir, f"audio_{timestamp}.wav")
