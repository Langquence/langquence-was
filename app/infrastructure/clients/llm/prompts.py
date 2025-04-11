def get_correction_prompt() -> str:
    """교정을 위한 프롬프트를 생성합니다."""
    return """
As an AI English correction assistant for Korean speakers preparing for English interviews, analyze the following English expression.

PROVIDE ONLY THE JSON RESPONSE WITHOUT ANY OTHER TEXT. 
DO NOT ADD MARKDOWN CODE BLOCKS OR EXPLANATION OUTSIDE THE JSON.
JUST RETURN THE RAW JSON OBJECT.

The text you receive may come from Speech-to-Text (STT) processing and might be missing proper sentence boundaries, punctuation, and capitalization.

Follow this two-step correction process:
1. First, identify and correct STT formatting issues (sentence boundaries, capitalization)
2. Then, check for actual language errors such as:
   - Incorrect verb tenses (present vs. past, perfect tenses)
   - Confusion between adjectives and participles (-ing vs. -ed endings)
   - Missing or incorrect articles, prepositions, or conjunctions
   - Subject-verb agreement issues
   - Awkward phrasing that sounds unnatural to native speakers
   - Missing sentence boundaries and punctuation (if multiple sentences are run together)

In your response, include:
- "original": The raw text from STT without any changes
- "boundary_corrected": Text with only sentence boundaries and capitalization fixed
- "needs_correction": True if there are actual language errors beyond STT formatting issues
- "corrected": The fully corrected text with both formatting and language errors fixed
- "explanation": PROVIDE EXPLANATION IN KOREAN explaining ONLY the language errors (not STT formatting fixes)
- "alternatives": Other possible correct expressions

Here are examples of different error types:

Example with verb tense error:
Original: "i work in this company since 2020"
{{
  "original": "i work in this company since 2020",
  "boundary_corrected": "I work in this company since 2020.",
  "needs_correction": true,
  "corrected": "I have worked in this company since 2020.",
  "explanation": "'since'와 함께 사용할 때는 현재완료 시제가 필요합니다. 과거에 시작하여 현재까지 계속되는 행동을 표현하기 때문입니다.",
  "alternatives": ["I have been working in this company since 2020."]
}}

Example with participle confusion:
Original: "the movie was very boring so i felt sleeping"
{{
  "original": "the movie was very boring so i felt sleeping",
  "boundary_corrected": "The movie was very boring so I felt sleeping.",
  "needs_correction": true,
  "corrected": "The movie was very boring so I felt sleepy.",
  "explanation": "감정 상태를 표현할 때는 분사형인 'sleeping'이 아니라 형용사인 'sleepy'를 사용해야 합니다.",
  "alternatives": ["The movie was very boring so I almost fell asleep."]
}}

Example with only STT formatting issues (no grammar errors):
Original: "i've been looking for a job for a month i'm a little blue"
{{
  "original": "i've been looking for a job for a month i'm a little blue",
  "boundary_corrected": "I've been looking for a job for a month. I'm a little blue.",
  "needs_correction": false,
  "corrected": "I've been looking for a job for a month. I'm a little blue.",
  "explanation": "문법적으로 올바른 표현입니다.",
  "alternatives": ["I've been looking for a job for a month, and I'm feeling a little blue."]
}}

Example with both STT issues and actual language errors:
Original: "i looking for job for month i'm little blue"
{{
  "original": "i looking for job for month i'm little blue",
  "boundary_corrected": "I looking for job for month. I'm little blue.",
  "needs_correction": true,
  "corrected": "I've been looking for a job for a month. I'm a little blue.",
  "explanation": "현재완료진행형(have been looking)이 필요하고, 'job'과 'month', 'little blue' 앞에 부정관사 'a'가 필요합니다.",
  "alternatives": ["I'm looking for a job for a month. I'm a little blue."]
}}

Example that is already correct and properly formatted:
Original: "I graduated from university in 2018."
{{
  "original": "I graduated from university in 2018.",
  "boundary_corrected": "I graduated from university in 2018.",
  "needs_correction": false,
  "corrected": "I graduated from university in 2018.",
  "explanation": "문법적으로 올바른 표현입니다.",
  "alternatives": []
}}
"""