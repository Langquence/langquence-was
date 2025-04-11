import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.clients.llm.alibaba.qwen_client import QwenTurboClient
from app.infrastructure.clients.llm.llm_client import LlmClient
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture
def mock_openai_response():
    """OpenAI 응답을 모킹하는 픽스처"""
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="""
                {
                  "original": "i looking for job for month",
                  "boundary_corrected": "I looking for job for month.",
                  "needs_correction": true,
                  "corrected": "I've been looking for a job for a month.",
                  "explanation": "현재완료진행형(have been looking)이 필요하고, 'job'과 'month' 앞에 부정관사 'a'가 필요합니다.",
                  "alternatives": ["I'm looking for a job for a month."]
                }
                """
            )
        )
    ]
    return mock_response

@pytest.mark.asyncio
async def test_correct_text(mock_openai_response):
    """LLM 클라이언트 correct_text 함수 테스트"""
    # given
    client = QwenTurboClient()
    
    with patch.object(client.client.chat.completions, 'create', return_value=mock_openai_response):
        result = await client.correct_text("i looking for job for month")
    
    # then
    assert result.original == "i looking for job for month"
    assert result.needs_correction == True
    assert result.corrected == "I've been looking for a job for a month."
    assert "현재완료진행형" in result.explanation
    assert result.alternatives == ["I'm looking for a job for a month."]

@pytest.mark.parametrize("input_text,expected_response", [
    (
        "i looking for job for month", 
        {
            "needs_correction": True,
            "expected_explanation_substr": "현재완료진행형",
            "boundary_corrected": "I looking for job for month."
        }
    ),
    (
        "i work here since 2020", 
        {
            "needs_correction": True,
            "expected_explanation_substr": "현재완료",
            "boundary_corrected": "I work here since 2020."
        }
    ),
    (
        "i've been looking for a job for a month i'm a little blue", 
        {
            "needs_correction": False,
            "expected_explanation_substr": "올바른 표현",
            "boundary_corrected": "I've been looking for a job for a month. I'm a little blue."
        }
    )
])
@pytest.mark.asyncio
async def test_correction_scenarios(input_text, expected_response, monkeypatch):
    """
    다양한 교정 시나리오 통합 테스트 (실제 API 호출 모킹)
    
    주의! 이 테스트는 실제 프롬프트를 테스트하기 위해 모킹 대신 실제 API를 호출할 수도 있습니다.
    """

    # given
    client = QwenTurboClient()
    
    # when
    result = await client.correct_text(input_text)
    logger.info(f"result: {result}")

    # then
    assert result.original == input_text
    assert result.boundary_corrected == expected_response["boundary_corrected"]
    assert result.needs_correction == expected_response["needs_correction"]
    assert expected_response["expected_explanation_substr"] in result.explanation
