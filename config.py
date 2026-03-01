import os
from pathlib import Path

class Config:
    """XTTS-v2 proje konfigürasyonu."""
    
    # Model ayarları
    MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # Dil seçenekleri
    SUPPORTED_LANGUAGES = ["tr", "en", "es", "fr", "de", "it", "pt", "pl", "cs", "ar", "ru", "hu", "ko", "ja", "hi", "zh-cn"]
    
    # Çıktı dizini
    OUTPUT_DIR = Path("outputs")
    SAMPLES_DIR = Path("samples")
    
    # GPU ayarları
    USE_GPU = True  # Otomatik algılanacak
    
    @classmethod
    def init_dirs(cls):
        """Dizinleri oluşturur."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.SAMPLES_DIR.mkdir(exist_ok=True)
