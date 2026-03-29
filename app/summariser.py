import os
from dotenv import load_dotenv
import anthropic
from .models import NoteRequest, SummaryResponse, RiskFlag

load_dotenv(override=False)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = "You are a clinical decision support assistant. Analyse the clinical note and call the analyse_note tool with your findings."

_TOOL = {
    "name": "analyse_note",
    "description": "Return a structured analysis of a clinical note.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "2-3 sentence plain-English summary of the note."
            },
            "key_findings": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of notable clinical findings."
            },
            "risk_flags": {
                "type": "array",
                "description": "List of clinical risk concerns.",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["medication", "vital_signs", "symptom", "allergy", "other"]
                        },
                        "detail": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["high", "medium", "low"]
                        }
                    },
                    "required": ["category", "detail", "severity"]
                }
            },
            "recommended_actions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Suggested next steps or clinical actions."
            }
        },
        "required": ["summary", "key_findings", "risk_flags", "recommended_actions"]
    }
}


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
        tools=[_TOOL],
        tool_choice={"type": "tool", "name": "analyse_note"},
        messages=[{"role": "user", "content": context}]
    )

    tool_block = next(b for b in message.content if b.type == "tool_use")
    data = tool_block.input

    return SummaryResponse(
        summary=data["summary"],
        key_findings=data["key_findings"],
        risk_flags=[RiskFlag(**f) for f in data.get("risk_flags", [])],
        recommended_actions=data.get("recommended_actions", [])
    )
