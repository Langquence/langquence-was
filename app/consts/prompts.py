def get_correction_prompt() -> str:
    """교정을 위한 프롬프트를 생성합니다."""
    return """
As an AI English correction assistant for Korean speakers preparing for English interviews,
analyze the following English expression.

PROVIDE ONLY THE JSON RESPONSE WITHOUT ANY OTHER TEXT. 
DO NOT ADD MARKDOWN CODE BLOCKS OR EXPLANATION OUTSIDE THE JSON.
JUST RETURN THE RAW JSON OBJECT.

Check for these common error patterns in English expressions:
- Incorrect verb tenses (present vs. past, perfect tenses)
- Confusion between adjectives and participles (-ing vs. -ed endings)
- Missing or incorrect articles, prepositions, or conjunctions
- Subject-verb agreement issues
- Awkward phrasing that sounds unnatural to native speakers

Here are examples of different error types:

Example with verb tense error:
Original: "I work in this company since 2020."
{{
  "original": "I work in this company since 2020.",
  "needs_correction": true,
  "corrected": "I have worked in this company since 2020.",
  "explanation": "With 'since' we need present perfect tense to describe an action that started in the past and continues to the present.",
  "alternatives": ["I have been working in this company since 2020."]
}}

Example with participle confusion:
Original: "The movie was very boring so I felt sleeping."
{{
  "original": "The movie was very boring so I felt sleeping.",
  "needs_correction": true,
  "corrected": "The movie was very boring so I felt sleepy.",
  "explanation": "We use 'sleepy' (adjective) to describe the feeling, not 'sleeping' (participle).",
  "alternatives": ["The movie was very boring so I almost fell asleep."]
}}

Example that is already correct:
Original: "I graduated from university in 2018."
{{
  "original": "I graduated from university in 2018.",
  "needs_correction": false,
  "corrected": "I graduated from university in 2018.",
  "explanation": "This expression is already natural and grammatically correct.",
  "alternatives": []
}}
"""