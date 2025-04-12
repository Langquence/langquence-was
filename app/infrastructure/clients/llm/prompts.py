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
3. For each identified error in a sentence, provide detailed correction information

In your response, include:
- "original": The raw text from STT without any changes
- "boundary_corrected": Text with only sentence boundaries and capitalization fixed
- "needs_correction": True if there are actual language errors beyond STT formatting issues
- "corrected": The fully corrected text for this sentence (empty string if needs_correction is false)
- "explanation": Array of error objects, each containing:
  * "error": The specific error text
  * "correct": The corrected version of that specific text
  * "reason": Brief explanation in Korean why correction is needed
- "alternatives": Other possible correct expressions (empty array if needs_correction is false)

IMPORTANT: If needs_correction is false, return empty values for "corrected", "explanation", and "alternatives" to save tokens.

Here are examples of different error types:

Example with verb tense error:
Original: "i'm looking for job for a month i'm little blue"
[
  {
    "original": "i'm looking for job for a month",
    "boundary_corrected": "I'm looking for job for a month.",
    "needs_correction": true,
    "corrected": "I've been looking for a job for a month.",
    "explanation": [
      {
        "error": "I'm looking",
        "correct": "I've been looking",
        "reason": "특정 기간('for a month') 동안 계속된 행동을 표현할 때는 현재완료진행형이 더 자연스럽습니다."
      },
      {
        "error": "for job",
        "correct": "for a job",
        "reason": "가산명사 'job' 앞에는 부정관사 'a'가 필요합니다."
      }
    ],
    "alternatives": ["I'm searching for a job for a month."]
  },
  {
    "original": "i'm little blue",
    "boundary_corrected": "I'm little blue.",
    "needs_correction": true,
    "corrected": "I'm a little blue.",
    "explanation": [
      {
        "error": "little blue",
        "correct": "a little blue",
        "reason": "'little'이 형용사로 사용될 때 'a little'의 형태로 사용되어야 합니다."
      }
    ],
    "alternatives": ["I'm feeling a bit down."]
  }
]

Example with only STT formatting issues (no grammar errors):
Original: "i graduated from university in 2018 i'm looking for my first job"
[
  {
    "original": "i graduated from university in 2018",
    "boundary_corrected": "I graduated from university in 2018.",
    "needs_correction": false,
    "corrected": "",
    "explanation": [],
    "alternatives": []
  },
  {
    "original": "i'm looking for my first job",
    "boundary_corrected": "I'm looking for my first job.",
    "needs_correction": false,
    "corrected": "",
    "explanation": [],
    "alternatives": []
  }
]

Example with mixed corrections:
Original: "i work here since 2020 i love my job"
[
  {
    "original": "i work here since 2020",
    "boundary_corrected": "I work here since 2020.",
    "needs_correction": true,
    "corrected": "I have worked here since 2020.",
    "explanation": [
      {
        "error": "I work",
        "correct": "I have worked",
        "reason": "'since'와 함께 사용할 때는 현재완료 시제가 필요합니다. 과거에 시작하여 현재까지 계속되는 행동을 표현하기 때문입니다."
      }
    ],
    "alternatives": ["I have been working here since 2020."]
  },
  {
    "original": "i love my job",
    "boundary_corrected": "I love my job.",
    "needs_correction": false,
    "corrected": "",
    "explanation": [],
    "alternatives": []
  }
]
"""