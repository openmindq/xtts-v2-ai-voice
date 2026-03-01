"""Özel hata sınıfları XTTS Voice projesi için."""

from typing import Optional


class XTTSVoiceError(Exception):
    """Temel XTTS Voice hatası."""


class ModelLoadError(XTTSVoiceError):
    """Model yükleme hatası."""


class SynthesisError(XTTSVoiceError):
    """Ses sentezleme hatası."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause


class SpeakerFileError(XTTSVoiceError):
    """Ses örneği dosyası hatası."""
