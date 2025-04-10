from app.common.utils.logger import get_logger
from pydantic import BaseModel
from typing import List

logger = get_logger(__name__)

class PatternMatchingCommand(BaseModel):
    original: str
    needs_correction: bool

class PatternMatchingResult(BaseModel):
    original: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []

async def validate_correction(correction: PatternMatchingCommand) -> PatternMatchingResult:
    """
    Validates and improves the correction result.

    Args:
        correction (PatternMatchingCommand): The correction result to validate.

    Returns:
        PatternMatchingResult: The validated and improved correction result.

    Todo:
        * Implement pattern matching logic.
        * This function may be used at the sentence level in the future.
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
    """
    Checks for common grammatical errors in the text.

    Args:
        text (str): The text to check.

    Returns:
        bool: True if errors are found, False otherwise.
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

def correct_common_errors(correction: PatternMatchingCommand) -> PatternMatchingResult:
    """
    Corrects common errors in the correction result.

    Args:
        correction (PatternMatchingCommand): The correction result to improve.

    Returns:
        PatternMatchingResult: The corrected correction result.
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
            logger.info(f"Corrected common error: {error} -> {correction}")
            break
    
    return PatternMatchingResult(
        original=text,
        needs_correction=needs_correction,
        corrected=corrected,
        explanation=explanation,
        alternatives=alternatives
    )