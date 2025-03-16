from fastapi import HTTPException
from typing import Dict, Any
import requests

from services.speech_recognizer_protocol import SpeechRecognizer

class NaverClovaSpeechRecognizer(SpeechRecognizer):
    """네이버 Clova 음성 인식 API를 이용한 음성 인식"""

    def __init__(self, client_id: str, client_secret: str, api_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url

    def recognize(self, audio_data: bytes, language: str = "Eng") -> Dict[str, Any]:
        """음성 데이터를 텍스트로 변환"""
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.api_key_id,
            "X-NCP-APIGW-API-KEY": self.api_key,
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
        
        if response.status_code != 200:
            error_message = response.text
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API 호출 오류: {error_message}"
            )
    
        return response.json()