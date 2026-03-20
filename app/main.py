from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import NoteRequest, SummaryResponse
from .summariser import analyse_note

app = FastAPI(
    title="Clinical Note Summariser",
    description="AI-powered clinical note analysis with risk flagging",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Clinical Note Summariser API"}

@app.get("/debug")
def debug():
    import os
    key = os.getenv("ANTHROPIC_API_KEY")
    return {"key_set": key is not None, "key_preview": key[:10] if key else "NOT FOUND"}

@app.post("/summarise", response_model=SummaryResponse)
def summarise_note(request: NoteRequest):
    try:
        return analyse_note(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))