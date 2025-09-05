import json

from openai import OpenAI

from featback.config import settings

try:
    client = OpenAI(api_key=settings.openai_api_key)
except Exception:
    client = None

JSON_SCHEMA = {
  "name": "extractions",
  "schema": {
    "type": "object",
    "properties": {
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": {"type": "string", "enum": ["review", "question"]},
            "category": {"type": "string"},
            "feature": {"type": "string"},
            "emotion": {"type": "string"},
            "reason": {"type": "string"}
          },
          "required": ["type","category","feature","reason"],
          "additionalProperties": False
        }
      }
    },
    "required": ["items"],
    "additionalProperties": False
  }
}

PROMPT_TMPL = """You are extracting structured insights from a Reddit post about: {product}
Title: "{title}"
Post: "{text}"
If review: type="review", category, feature, emotion, reason.
If question: type="question", category, feature, reason (no emotion).
If irrelevant: emit zero items.
Categories: Battery, Camera, Display, Performance, Connectivity, Design, Software.
Emotions: Excitement, Satisfaction, Joy, Relief, Trust, Disappointment, Frustration, Anger, 
Confusion, Regret, Curiosity, Surprise, Skepticism, Indifference, Anticipation.
Reasons: Below Expectations, Above Expectations, Functionality, Reliability, Ease of use, 
Accessibility, Design, Build quality, Overheating, Compatibility.
Respond ONLY with JSON per the schema.
"""

def extract_features(title: str, text: str, product: str) -> list[dict]:
    if client is None:
        return []
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_schema", "json_schema": JSON_SCHEMA},
            messages=[
                {
                    "role": "system",
                    "content": "Extract structured insights exactly as per the schema."
                },
                {"role":"user","content":PROMPT_TMPL.format(title=title,text=text,product=product)},
            ],
            max_tokens=900
        )
        data = json.loads(resp.choices[0].message.content)
        return data.get("items", [])
    except Exception:
        return []
