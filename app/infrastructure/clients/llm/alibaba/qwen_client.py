import json
from openai import OpenAI
from app.config.app_config import settings
from app.infrastructure.clients.llm.prompts import get_correction_prompt
from app.infrastructure.clients.llm.llm_client import LlmClient, LlmResponse
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

class QwenTurboClient(LlmClient):
    """Alibaba Tongyi 모델을 사용하는 LLM 서비스"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.ALIBABA_API_KEY,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )

    """LLM API를 호출하여 텍스트를 교정합니다."""
    async def correct_text(self, input_text: str) -> LlmResponse:
        prompt = get_correction_prompt()
        
        try:
            completion = self.client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=settings.MAX_TOKENS
            )
            logger.info(f"API response: \n{completion}")
            
            result = completion.choices[0].message.content
            
            parsed_result = self.parse_llm_response(result, input_text)
            return parsed_result
            
        except Exception as e:
            logger.error(f"API call failed: {e}")

            return LlmResponse(
                original=input_text,
                needs_correction=False,
                corrected=input_text,
                explanation=f"API call failed: {str(e)}",
                alternatives=[]
            )

    """LLM 응답을 파싱합니다."""
    def parse_llm_response(self, response: str, input_text: str) -> LlmResponse:
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
            
            return LlmResponse(
                original=result.get("original", input_text),
                needs_correction=result.get("needs_correction", False),
                corrected=result.get("corrected", input_text),
                explanation=result.get("explanation", "No explanation provided"),
                alternatives=result.get("alternatives", [])
            )
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            return LlmResponse(
                original=input_text,
                needs_correction=False,
                corrected=input_text,
                explanation="Failed to parse model response",
                alternatives=[]
            )