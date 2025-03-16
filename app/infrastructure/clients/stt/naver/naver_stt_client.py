from fastapi import HTTPException
from typing import Dict, Any
import requests

from app.infrastructure.clients.stt.speech_recognizer import SpeechRecognizer
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

class NaverClovaSpeechRecognizer(SpeechRecognizer):
    """네이버 Clova 음성 인식 API를 이용한 음성 인식"""

    def __init__(self, client_id: str, client_secret: str, api_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url

    async def recognize(self, audio_data: bytes, language: str = "Eng") -> Dict[str, Any]:
        """음성 데이터를 텍스트로 변환"""
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
            "Content-Type": "application/octet-stream"
        }
        
        params = {
            "lang": language
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            params=params,
            data=audio_data
        )

        logger.info(f"STT API 호출 결과: {response.text}")
        
        if response.status_code != 200:
            error_message = response.text
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API 호출 오류: {error_message}"
            )
    
        return response.json()