import json
from openai import OpenAI
from app.config.app_config import settings
from app.infrastructure.clients.llm.prompts import get_correction_prompt
from app.infrastructure.clients.llm.llm_client import LlmClient, LlmResponse, SentenceCorrection, CorrectionDetail
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
            
            parsed_result = self._parse_llm_response(result, input_text)
            return parsed_result
            
        except Exception as e:
            logger.error(f"API call failed: {e}")

            sentence = SentenceCorrection(
                original=input_text,
                boundary_corrected=input_text,
                needs_correction=False,
                corrected="",
                explanation=[],
                alternatives=[]
            )
        
            return LlmResponse(
                sentences=[sentence], 
                error=f"API call failed: {str(e)}"
            )

    """LLM 응답을 파싱합니다."""
    def _parse_llm_response(self, response: str, input_text: str) -> LlmResponse:
        logger.debug(f"Parsing response: {response}")
        
        try:
            start_idx = response.find('[')
            if start_idx == -1:
                raise ValueError("No JSON found in response")
                
            end_idx = response.rfind(']')
            if end_idx == -1 or end_idx < start_idx:
                raise ValueError("Invalid JSON structure")
                
            json_str = response[start_idx:end_idx+1]
            result_array = json.loads(json_str)
            
            sentences = []
            for item in result_array:
                # CorrectionDetail 객체로 explanation 변환
                explanation_list = [
                    CorrectionDetail(**exp) for exp in item.get("explanation", [])
                ]
                
                sentence = SentenceCorrection(
                    original=item.get("original", ""),
                    boundary_corrected=item.get("boundary_corrected", ""),
                    needs_correction=item.get("needs_correction", False),
                    corrected=item.get("corrected", ""),
                    explanation=explanation_list,
                    alternatives=item.get("alternatives", [])
                )
                sentences.append(sentence)
            
                return LlmResponse(sentences=sentences)
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            return LlmResponse(
                original=input_text,
                boundary_corrected=input_text,
                needs_correction=False,
                corrected=input_text,
                explanation="Failed to parse model response",
                alternatives=[]
            )