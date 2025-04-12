import pytest
from unittest.mock import patch, MagicMock
from app.infrastructure.clients.llm.alibaba.qwen_client import QwenTurboClient
from app.infrastructure.clients.llm.llm_client import LlmClient, LlmResponse, SentenceCorrection, CorrectionDetail
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
                [
                  {
                    "original": "i looking for job for month",
                    "boundary_corrected": "I looking for job for month.",
                    "needs_correction": true,
                    "corrected": "I've been looking for a job for a month.",
                    "explanation": [
                      {
                        "error": "I looking",
                        "correct": "I've been looking",
                        "reason": "현재완료진행형(have been looking)이 필요합니다."
                      },
                      {
                        "error": "for job",
                        "correct": "for a job",
                        "reason": "'job' 앞에 부정관사 'a'가 필요합니다."
                      },
                      {
                        "error": "for month",
                        "correct": "for a month",
                        "reason": "'month' 앞에 부정관사 'a'가 필요합니다."
                      }
                    ],
                    "alternatives": ["I'm looking for a job for a month."]
                  }
                ]
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
    assert len(result.sentences) == 1
    sentence = result.sentences[0]
    assert sentence.original == "i looking for job for month"
    assert sentence.needs_correction == True
    assert sentence.corrected == "I've been looking for a job for a month."
    
    explanation_reasons = [detail.reason for detail in sentence.explanation]
    assert any("현재완료진행형" in reason for reason in explanation_reasons)
    assert any("부정관사 'a'" in reason for reason in explanation_reasons)
    
    assert sentence.alternatives == ["I'm looking for a job for a month."]

@pytest.mark.parametrize("input_text,expected_response", [
    (
        "i've looking for job for a month", 
        {
            "sentences": [
                {
                    "original": "i've looking for job for a month",
                    "boundary_corrected": "I've looking for job for a month.",
                }
            ],
            "sentence_count": 1
        },
    ),
    (
        "i've been looking for a job for a month i'm a little blue", 
        {
            "sentences": [
                {
                    "original": "i've been looking for a job for a month",
                    "boundary_corrected": "I've been looking for a job for a month.",
                },
                {
                    "original": "i'm a little blue",
                    "boundary_corrected": "I'm a little blue.",
                }
            ],
            "sentence_count": 2
        }
    ),
    (
        "i'm looking for job for a month i'm little blue i'm going to get some fresh air", 
        {
            "sentences": [
                {
                    "original": "i'm looking for job for a month",
                    "boundary_corrected": "I'm looking for job for a month.",
                },
                {
                    "original": "i'm little blue",
                    "boundary_corrected": "I'm little blue.",
                },
                {
                    "original": "i'm going to get some fresh air",
                    "boundary_corrected": "I'm going to get some fresh air.",
                }
            ],
            "sentence_count": 3
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

    # then
    for i, expected_sentence in enumerate(expected_response["sentences"]):
        actual_sentence = result.sentences[i]
        
        # 원본 텍스트 확인
        assert actual_sentence.original == expected_sentence["original"], f"원본 텍스트가 일치하지 않습니다. 예상: {expected_sentence['original']}, 실제: {actual_sentence.original}"
        
        # boundary_corrected 확인
        assert actual_sentence.boundary_corrected == expected_sentence["boundary_corrected"], f"경계 교정 텍스트가 일치하지 않습니다. 예상: {expected_sentence['boundary_corrected']}, 실제: {actual_sentence.boundary_corrected}"