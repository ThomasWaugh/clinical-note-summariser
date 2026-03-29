from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
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

_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(_static_dir, "index.html"))



@app.post("/summarise", response_model=SummaryResponse)
def summarise_note(request: NoteRequest):
    try:
        return analyse_note(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))