import os
from celery import Celery
from .core.engine import XTTSEngineV2

# Redis üzerinden Celery konfigürasyonu
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("xtts_worker", broker=redis_url, backend=redis_url)

# Engine'i worker seviyesinde başlat (singleton olarak)
engine = XTTSEngineV2()

@celery_app.task(name="synthesize_task")
def synthesize_task(text: str, speaker_wav: str, language: str, output_path: str):
    """Arka planda ses sentezleme görevi."""
    return str(engine.synthesize_to_file(text, speaker_wav, language, output_path))
