from app.api.dto.correct_dto import CorrectionResponse, CorrectionDetail as ApiCorrectionDetail, SentenceCorrection as ApiSentenceCorrection
from app.infrastructure.clients.llm.llm_client import LlmResponse, CorrectionDetail as LlmCorrectionDetail, SentenceCorrection as LlmSentenceCorrection

def to_correction_response(id: int,data: LlmResponse) -> CorrectionResponse:
    sentences = [
        ApiSentenceCorrection(
            original=sentence.original,
            boundary_corrected=sentence.boundary_corrected,
            needs_correction=sentence.needs_correction,
            corrected=sentence.corrected,
            explanation=[to_correction_detail(detail) for detail in sentence.explanation],
            alternatives=sentence.alternatives
        ) 
        for sentence in data.sentences
    ]
    return CorrectionResponse(id=id, sentences=sentences)

def to_correction_detail(data: LlmCorrectionDetail) -> ApiCorrectionDetail:
    return ApiCorrectionDetail(
        error=data.error, 
        correct=data.correct, 
        reason=data.reason
    )