import os
import json
from openai import OpenAI
from app.config.app_config import settings
from app.consts.prompts import get_correction_prompt
from app.dto.schemas import CorrectionResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

client = OpenAI(
    api_key=settings.ALIBABA_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

"""LLM API를 호출하여 텍스트를 교정합니다."""
async def correct_text(input_text: str) -> CorrectionResponse:
    prompt = get_correction_prompt(input_text)
    
    try:
        completion = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            max_tokens=settings.MAX_TOKENS
        )
        logger.info(f"API response: \n {completion}")
        
        result = completion.choices[0].message.content
        
        parsed_result = parse_llm_response(result, input_text)
        return parsed_result
            
    except Exception as e:
        logger.error(f"API call failed: {e}")

        return CorrectionResponse(
            original=input_text,
            needs_correction=False,
            corrected=input_text,
            explanation=f"API call failed: {str(e)}",
            alternatives=[]
        )

"""LLM 응답을 파싱합니다."""
def parse_llm_response(response: str, input_text: str) -> CorrectionResponse:
    logger.debug(f"Parsing response: {response}")
    
    try:
        start_idx = response.find('{')
        if start_idx == -1:
            raise ValueError("No JSON found in response")
            
        end_idx = response.rfind('}')
        if end_idx == -1 or end_idx < start_idx:
            raise ValueError("Invalid JSON structure")
            
        json_str = response[start_idx:end_idx+1]
        result = json.loads(json_str)
        
        return CorrectionResponse(
            original=result.get("original", input_text),
            needs_correction=result.get("needs_correction", False),
            corrected=result.get("corrected", input_text),
            explanation=result.get("explanation", "No explanation provided"),
            alternatives=result.get("alternatives", [])
        )
    except Exception as e:
        logger.error(f"Failed to parse response: {e}")
        return CorrectionResponse(
            original=input_text,
            needs_correction=False,
            corrected=input_text,
            explanation="Failed to parse model response",
            alternatives=[]
        )