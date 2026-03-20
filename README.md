# Clinical Note Summariser

An AI-powered clinical note analysis API built with FastAPI and Claude (Anthropic). Accepts free-text clinical notes and returns structured summaries, key findings, risk flags, and recommended actions.

Built to demonstrate the combination of biomedical domain knowledge and modern AI engineering.

## What it does

- Accepts unstructured clinical notes as input
- Returns a structured JSON response containing:
  - Plain-English summary
  - Key clinical findings
  - Risk flags with severity ratings (high / medium / low)
  - Recommended clinical actions

## Tech stack

- Python / FastAPI
- Anthropic Claude API
- Docker
- Pydantic for data validation
- Deployed live on Render — https://clinical-note-summariser.onrender.com

## Example input
```json
{
  "note": "68F presenting with chest tightness and shortness of breath onset 2hrs ago. Hx: T2DM on Metformin, hypertension on Lisinopril. Scheduled CT with contrast tomorrow. SpO2 92% on room air. BP 158/94. Bilateral crackles on auscultation.",
  "patient_age": 68,
  "patient_sex": "female"
}
```

## Example output
```json
{
  "summary": "68-year-old female presenting with acute onset chest tightness and shortness of breath with hypoxia and bilateral crackles, suggesting possible acute pulmonary edema or decompensated heart failure.",
  "key_findings": [
    "SpO2 92% on room air — clinically significant hypoxia",
    "BP 158/94 mmHg — uncontrolled hypertension",
    "Bilateral crackles — suggestive of pulmonary edema"
  ],
  "risk_flags": [
    {
      "category": "medication",
      "detail": "Metformin must be held before and 48 hours after iodinated contrast CT due to risk of lactic acidosis",
      "severity": "high"
    },
    {
      "category": "vital_signs",
      "detail": "SpO2 92% on room air indicates hypoxia requiring immediate supplemental oxygen",
      "severity": "high"
    }
  ],
  "recommended_actions": [
    "Initiate supplemental oxygen immediately to target SpO2 ≥ 95%",
    "Hold Metformin immediately given planned contrast CT",
    "Obtain urgent 12-lead ECG to rule out ACS"
  ]
}
```

## Running locally
```bash
git clone https://github.com/ThomasWaugh/clinical-note-summariser.git
cd clinical-note-summariser
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` to explore the API.

## Background

Built as part of a health tech AI portfolio targeting clinical decision support applications. The biomedical domain knowledge (T2DM management, contrast contraindications, ACE inhibitor monitoring) is intentionally embedded in the prompt design — not just generic summarisation.
