from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from .tts_engine import TTSEngine

app = FastAPI(title="XTTS-v2 Voice API")
engine = TTSEngine()

class SynthesisRequest(BaseModel):
    text: str
    language: str = "tr"
    speaker_wav: str = None

@app.post("/synthesize")
async def synthesize(request: SynthesisRequest):
    try:
        output_path = engine.synthesize(
            text=request.text,
            language=request.language,
            speaker_wav=Path(request.speaker_wav) if request.speaker_wav else None
        )
        return {"status": "success", "file": str(output_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
