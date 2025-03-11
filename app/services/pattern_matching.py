from app.dto.schemas import CorrectionResponse
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

async def validate_correction(correction: CorrectionResponse) -> CorrectionResponse:
    """교정 결과를 검증하고 개선합니다.
    
    Args:
        correction (CorrectionResponse): 교정 결과
    
    Returns:
        CorrectionResponse: 검증 및 개선된 교정 결과

    Todo:
        * 패턴 매칭 로직을 구현합니다.

    """
    logger.info(f"Validating correction for: {correction.original}")
    
    # 추가 패턴 매칭 로직을 구현해야 하는 부분
    # 예: 특정 문법 오류 패턴 체크, 응답 개선 등
    
    # 임시로 구현한 검증 로직
    if not correction.needs_correction and should_be_corrected(correction.original):
        logger.warning(f"Model failed to detect error in: {correction.original}")

        return correct_common_errors(correction)
    
    return correction

def should_be_corrected(text: str) -> bool:
    """텍스트에 흔한 문법 오류가 있는지 확인합니다.
    
    Args:
        text (str): 텍스트

    Returns:
        bool: 오류가 있는 경우 True, 없는 경우 False
    """

    common_errors = [
        ("I have work", "I have worked"),
        ("I am interesting in", "I am interested in"),
        ("I am boring", "I am bored"),
        ("since [0-9]+ years", "for [0-9]+ years"),
    ]
    
    for error_pattern, _ in common_errors:
        if error_pattern in text.lower():
            return True
    
    return False

def correct_common_errors(correction: CorrectionResponse) -> CorrectionResponse:
    """흔한 오류를 수정합니다.
    
    Args:
        correction (CorrectionResponse): 교정 결과
    
    Returns:
        CorrectionResponse: 수정된 교정 결과
    """
    text = correction.original
    needs_correction = False
    corrected = text
    explanation = "This expression was corrected by the pattern matching engine."
    alternatives = []
    
    common_errors = [
        ("I have work", "I have worked", "Changed 'work' to 'worked' for correct present perfect tense."),
        ("I am interesting in", "I am interested in", "Changed 'interesting' to 'interested' for correct participle usage."),
        ("I am boring", "I am bored", "Changed 'boring' to 'bored' to correctly express feeling rather than causing boredom."),
    ]
    
    for error, correction, reason in common_errors:
        if error in text:
            corrected = text.replace(error, correction)
            explanation = reason
            needs_correction = True
            alternatives = [text.replace(error, correction) + " (recommended)"]
            break
    
    return CorrectionResponse(
        original=text,
        needs_correction=needs_correction,
        corrected=corrected,
        explanation=explanation,
        alternatives=alternatives
    )