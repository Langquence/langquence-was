import io
from typing import Dict, Any, Optional, Tuple

import numpy as np
import scipy.io.wavfile as wavfile

from app.common.utils.logger import get_logger

logger = get_logger(__name__)


def diagnose_wav_bytes(byte_data: bytes) -> Dict[str, Any]:
    """WAV 바이트 데이터를 분석하여 헤더 정보 추출"""
    if len(byte_data) < 44:  # WAV 헤더는 최소 44바이트
        return {"error": "Data too short for WAV header"}

    try:
        result = {}

        # 'RIFF' 체크
        if byte_data[0:4] != b'RIFF':
            return {"error": f"Invalid RIFF header: {byte_data[0:4]}"}

        result["chunk_size"] = int.from_bytes(byte_data[4:8], byteorder='little')

        # 'WAVE' 체크
        if byte_data[8:12] != b'WAVE':
            return {"error": f"Invalid WAVE marker: {byte_data[8:12]}"}

        # 'fmt ' 체크
        if byte_data[12:16] != b'fmt ':
            return {"error": f"Invalid fmt marker: {byte_data[12:16]}"}

        result["subchunk1_size"] = int.from_bytes(byte_data[16:20], byteorder='little')
        result["audio_format"] = int.from_bytes(byte_data[20:22], byteorder='little')
        result["num_channels"] = int.from_bytes(byte_data[22:24], byteorder='little')
        result["sample_rate"] = int.from_bytes(byte_data[24:28], byteorder='little')
        result["byte_rate"] = int.from_bytes(byte_data[28:32], byteorder='little')
        result["block_align"] = int.from_bytes(byte_data[32:34], byteorder='little')
        result["bits_per_sample"] = int.from_bytes(byte_data[34:36], byteorder='little')

        # 'data' 체크
        if byte_data[36:40] != b'data':
            return {"error": f"Invalid data marker: {byte_data[36:40]}"}

        result["subchunk2_size"] = int.from_bytes(byte_data[40:44], byteorder='little')
        result["data_size"] = len(byte_data) - 44

        return result
    except Exception as e:
        return {"error": f"Error analyzing WAV header: {str(e)}"}


def extract_wav_info(byte_data: bytes) -> Tuple[Optional[int], Optional[np.ndarray]]:
    """바이트 데이터에서 WAV 정보 추출 시도"""
    try:
        with io.BytesIO(byte_data) as wav_buffer:
            sampling_rate, data = wavfile.read(wav_buffer)
            return sampling_rate, data
    except Exception as e:
        logger.error(f"Error extracting WAV info: {str(e)}")
        return None, None


def is_valid_wav(byte_data: bytes) -> bool:
    """WAV 형식이 유효한지 확인합니다."""
    header_info = diagnose_wav_bytes(byte_data)
    return "error" not in header_info
