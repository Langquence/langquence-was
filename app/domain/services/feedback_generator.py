from app.common.utils.logger import get_logger

logger = get_logger(__name__)

async def generate_feedback(correction: str) -> str:
    """
    Generates user-friendly feedback from the correction result.

    Args:
        correction (str): The correction result string.

    Returns:
        str: The feedback-enhanced correction result.

    Todo:
        * Implement more complex feedback generation logic.
    """
    logger.info("Generating feedback for correction result")
    
    # if correction.needs_correction:
    #     correction.explanation = enhance_explanation(correction.explanation)
    
    return correction

def enhance_explanation(explanation: str) -> str:
    """
    Enhances the explanation to be more educational.

    Args:
        explanation (str): The original explanation string.

    Returns:
        str: The enhanced explanation string.

    Todo:
        * Add more educational content to the explanation.
    """
    if not explanation.endswith('.'):
        explanation += '.'
        
    enhanced = explanation + " This change will make your English sound more natural in interview settings."
    logger.info("Enhanced explanation generated")
    return enhanced