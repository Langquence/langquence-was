from app.common.utils.logger import get_logger

logger = get_logger(__name__)

async def generate_feedback(correction: CorrectionResponse) -> CorrectionResponse:
    """교정 결과로부터 사용자 친화적인 피드백을 생성합니다.
    
    Args:
        correction (CorrectionResponse): OpenAI 교정 결과

    Returns:
        CorrectionResponse: 피드백이 추가된 교정 결과

    Todo:
        * 더 복잡한 피드백 생성 로직을 구현합니다. (현재는 단순 응답 형식 가공)
    """
    logger.info("Generating feedback for correction result")
    
    if correction.needs_correction:
        correction.explanation = enhance_explanation(correction.explanation)
    
    return correction

def enhance_explanation(explanation: str) -> str:
    """설명을 더 교육적으로 강화합니다.
    
    Todo:
        * 더 많은 교육적인 설명을 추가해야 합니다.
    """
    if not explanation.endswith('.'):
        explanation += '.'
        
    enhanced = explanation + " This change will make your English sound more natural in interview settings."
    return enhanced