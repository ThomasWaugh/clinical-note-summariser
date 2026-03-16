import anthropic
import json
import os
from dotenv import load_dotenv
from .models import NoteRequest, SummaryResponse, RiskFlag

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a clinical decision support assistant. 
Analyse clinical notes and return structured JSON only — no prose, no markdown.
Your response must be valid JSON matching this exact schema:
{
  "summary": "2-3 sentence plain-English summary",
  "key_findings": ["finding 1", "finding 2"],
  "risk_flags": [
    {"category": "medication|vital_signs|symptom|allergy|other", 
     "detail": "specific concern", 
     "severity": "high|medium|low"}
  ],
  "recommended_actions": ["action 1", "action 2"]
}"""

def analyse_note(request: NoteRequest) -> SummaryResponse:
    context = f"Patient note:\n{request.note}"
    if request.patient_age:
        context += f"\nPatient age: {request.patient_age}"
    if request.patient_sex:
        context += f"\nPatient sex: {request.patient_sex}"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}]
    )

    raw = message.content[0].text
    print("RAW RESPONSE:", raw) 
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip() # add this line

    data = json.loads(raw)

    return SummaryResponse(
        summary=data["summary"],
        key_findings=data["key_findings"],
        risk_flags=[RiskFlag(**f) for f in data.get("risk_flags", [])],
        recommended_actions=data.get("recommended_actions", [])
    )