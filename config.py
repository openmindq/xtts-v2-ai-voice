import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """XTTS-v2 profesyonel konfigürasyon ayarları."""
    
    # Model ayarları
    model_name: str = Field(default="tts_models/multilingual/multi-dataset/xtts_v2")
    
    # Dil seçenekleri
    supported_languages: List[str] = Field(
        default_factory=lambda: ["tr", "en", "es", "fr", "de", "it", "pt", "pl", "cs", "ar", "ru", "hu", "ko", "ja", "hi", "zh-cn"]
    )
    
    # Dizinler
    output_dir: Path = Field(default_factory=lambda: Path("outputs"))
    samples_dir: Path = Field(default_factory=lambda: Path("samples"))
    
    # GPU ayarları
    use_gpu: bool = Field(default=True)
    
    # .env dosyasından yükle
    model_path: str = Field(default="", description="Özel model yolu (opsiyonel)")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Singleton konfigürasyon instance'ı döndürür."""
    return Settings()

# Dizinleri otomatik oluştur
settings = get_settings()
settings.output_dir.mkdir(exist_ok=True)
settings.samples_dir.mkdir(exist_ok=True)
