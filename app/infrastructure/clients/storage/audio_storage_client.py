from typing import Protocol


class AudioStorageClient(Protocol):
    """오디오 저장 클라이언트 인터페이스"""

    async def save_audio(self, audio_data: bytes, extension: str) -> str:
        """
        오디오 데이터를 저장

        Args:
            audio_data (bytes): 바이너리 오디오 데이터
            extension (str): 파일 확장자

        Returns:
            str: 저장된 파일 경로
        """
        ...
