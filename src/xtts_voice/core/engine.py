import torch
import logging
import time
from pathlib import Path
from typing import Optional, List, Generator
from TTS.api import TTS
from .exceptions import ModelLoadError, SynthesisError

logger = logging.getLogger(__name__)

class XTTSEngineV2:
    """Üretim seviyesi, streaming destekli XTTS-v2 motoru."""
    
    _instance = None
    _is_ready = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(XTTSEngineV2, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2", use_gpu: bool = True):
        if self._is_ready:
            return
            
        self.device = "cuda" if torch.cuda.is_available() and use_gpu else "cpu"
        self.model_name = model_name
        self.tts: Optional[TTS] = None
        
        try:
            logger.info(f"XTTS Model yükleniyor: {self.model_name} (Cihaz: {self.device})")
            start_time = time.time()
            
            # Bellek yönetimi ve optimizasyon
            if self.device == "cuda":
                torch.cuda.empty_cache()
                # FP16 desteği
                torch.set_default_dtype(torch.float16 if torch.cuda.is_bf16_supported() else torch.float32)
            
            self.tts = TTS(self.model_name, gpu=(self.device == "cuda"))
            self.tts.to(self.device)
            
            # Warmup: İlk yükleme sonrası modeli ısıt
            logger.info("Model warmup yapılıyor...")
            self._warmup()
            
            self._is_ready = True
            logger.info(f"Model {time.time() - start_time:.2f} saniyede hazır hale getirildi.")
            
        except Exception as e:
            logger.error(f"Kritik model yükleme hatası: {e}", exc_info=True)
            raise ModelLoadError(f"XTTS motoru başlatılamadı: {e}")

    def _warmup(self):
        """Modeli ilk çalıştırma gecikmesinden kurtarmak için boş bir girdi ile çalıştırır."""
        if self.tts:
            try:
                # Küçük bir dummy sentezleme
                self.tts.tts(text="Ready", speaker_wav="samples/ref.wav", language="en")
            except:
                pass

    def synthesize_stream(self, text: str, speaker_wav: str, language: str = "tr") -> Generator[bytes, None, None]:
        """Düşük gecikmeli ses sentezleme (Streaming)."""
        if not self.tts:
            raise SynthesisError("Model yüklü değil.")
            
        try:
            # Chunking/Streaming mantığı (TTS kütüphanesinin yeteneklerine göre simüle edilir veya doğrudan çağrılır)
            # Not: XTTS-v2'nin gerçek streaming yeteneği için TTS.tts_stream kullanılabilir.
            chunks = self.tts.tts_stream(
                text=text,
                language=language,
                speaker_wav=speaker_wav,
                stream_chunk_size=20
            )
            for chunk in chunks:
                yield chunk.tobytes()
        except Exception as e:
            logger.error(f"Streaming hatası: {e}")
            raise SynthesisError(f"Ses akışı başarısız: {e}")

    def synthesize_to_file(self, text: str, speaker_wav: str, language: str, output_path: Path) -> Path:
        """Tam ses sentezleme ve dosyaya kaydetme."""
        try:
            self.tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=str(output_path)
            )
            return output_path
        except Exception as e:
            logger.error(f"Sentezleme hatası: {e}")
            raise SynthesisError(f"Dosya sentezleme başarısız: {e}")
