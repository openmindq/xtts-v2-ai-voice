import time
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .core.engine import XTTSEngineV2
from .utils.cache import AudioCache

# Logger ve API kurulumu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="XTTS-v2 Production API",
    description="Yüksek performanslı, streaming destekli XTTS-v2 servisi",
    version="2.0.0"
)

# Servisler
engine = XTTSEngineV2()
cache = AudioCache()

class SynthesisRequest(BaseModel):
    text: str
    language: str = "tr"
    speaker_wav: str = "samples/ref.wav"
    use_cache: bool = True

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/health")
async def health_check():
    """Servis durumunu ve GPU durumunu kontrol eder."""
    import torch
    return {
        "status": "online",
        "device": engine.device,
        "cuda_available": torch.cuda.is_available(),
        "gpu_memory": f"{torch.cuda.memory_reserved() / 1e9:.2f} GB" if torch.cuda.is_available() else "0 GB"
    }

@app.post("/stream")
async def stream_audio(request: SynthesisRequest):
    """Metni ses akışına (streaming) dönüştürür."""
    try:
        # Önbellekte varsa akışı doğrudan dönmek yerine tam dosyayı dönebiliriz (optimizasyon)
        # Ama streaming gerçek zamanlılık içindir.
        return StreamingResponse(
            engine.synthesize_stream(
                text=request.text,
                language=request.language,
                speaker_wav=request.speaker_wav
            ),
            media_type="audio/wav"
        )
    except Exception as e:
        logger.error(f"Streaming endpoint hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize")
async def synthesize_file(request: SynthesisRequest):
    """Metni ses dosyasına dönüştürür (Cache destekli)."""
    try:
        # Önbellek kontrolü
        if request.use_cache:
            cached_file = cache.get(request.text, request.speaker_wav, request.language)
            if cached_file:
                return {"status": "success", "file": str(cached_file), "cached": True}

        # Sentezleme
        output_name = f"output_{int(time.time())}.wav"
        output_path = Path("outputs") / output_name
        output_path.parent.mkdir(exist_ok=True)
        
        result = engine.synthesize_to_file(
            text=request.text,
            language=request.language,
            speaker_wav=request.speaker_wav,
            output_path=output_path
        )
        
        # Önbelleğe al
        if request.use_cache:
            cache.set(request.text, request.speaker_wav, request.language, result)
            
        return {"status": "success", "file": str(result), "cached": False}
        
    except Exception as e:
        logger.error(f"Synthesize endpoint hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
