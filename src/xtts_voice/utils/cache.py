import hashlib
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class AudioCache:
    """Ses çıktıları için disk tabanlı önbellekleme sistemi."""
    
    def __init__(self, cache_dir: str = "cache/audio"):
        self.cache_path = Path(cache_dir)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ses önbelleği hazır: {self.cache_path.absolute()}")

    def _generate_hash(self, text: str, speaker: str, language: str, params: Dict[str, Any]) -> str:
        """İstek parametrelerine göre benzersiz bir hash üretir."""
        payload = {
            "text": text,
            "speaker": speaker,
            "language": language,
            "params": params
        }
        dump = json.dumps(payload, sort_keys=True)
        return hashlib.md5(dump.encode()).hexdigest()

    def get(self, text: str, speaker: str, language: str, **kwargs) -> Optional[Path]:
        """Önbellekte varsa dosya yolunu döner."""
        cache_id = self._generate_hash(text, speaker, language, kwargs)
        file_path = self.cache_path / f"{cache_id}.wav"
        
        if file_path.exists():
            logger.info(f"Önbellek isabeti: {cache_id}")
            return file_path
        return None

    def set(self, text: str, speaker: str, language: str, audio_path: Path, **kwargs) -> None:
        """Üretilen sesi önbelleğe kaydeder."""
        cache_id = self._generate_hash(text, speaker, language, kwargs)
        target_path = self.cache_path / f"{cache_id}.wav"
        
        if not target_path.exists():
            import shutil
            shutil.copy(audio_path, target_path)
            logger.info(f"Yeni ses önbelleğe alındı: {cache_id}")
