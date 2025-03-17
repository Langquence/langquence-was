from typing import Protocol, Dict, Any

class SpeechRecognizer(Protocol):
    """음성 인식 인터페이스"""

    async def recognize(self, audio_data: bytes, language: str) -> str:
        """
        음성 데이터를 텍스트로 변환
        
        Args:
            audio_data (bytes): 바이너리 오디오 데이터
            language (str): 언어 코드
        
        Returns:
            str: 변환된 텍스트

        Todo:
            * 일관된 예외 처리를 위한 예외 코드 객체가 필요합니다.
            * 반환 타입에 DTO를 정의하여 반환해야 합니다.
        """
        ...