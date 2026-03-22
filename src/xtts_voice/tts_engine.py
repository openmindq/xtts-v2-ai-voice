import torch
import logging
from pathlib import Path
from typing import Optional
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
# Import düzeltildi: Absolute import kullanıldı
from xtts_voice.settings import get_settings
from .exceptions import ModelLoadError, SynthesisError, SpeakerFileError

logger = logging.getLogger(__name__)

class TTSEngine:
    """XTTS-v2 TTS motoru - GPU/CPU destekli."""
    
    def __init__(self) -> None:
        self.settings = get_settings()
        self.device = 'cuda' if torch.cuda.is_available() and self.settings.use_gpu else 'cpu'
        logger.info(f'XTTS Engine başlatıldı. Cihaz: {self.device.upper()}')
        
        try:
            # Bellek yönetimi: GPU için boşaltma ve model yükleme
            if self.device == 'cuda':
                torch.cuda.empty_cache()
            
            self.tts = TTS(self.settings.model_name, gpu=(self.device == 'cuda'))
            self.tts.to(self.device)
            logger.info('XTTS-v2 modeli başarıyla yüklendi.')
        except Exception as e:
            logger.error(f'Model yükleme hatası: {e}')
            raise ModelLoadError(f'XTTS-v2 modeli yüklenemedi: {str(e)}', e)
    
    def synthesize(
        self,
        text: str,
        speaker_wav: Optional[Path] = None,
        language: str = 'tr',
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Metni sese dönüştürür.
        
        Args:
            text: Sentezlenecek metin (max 200 kelime önerilir).
            speaker_wav: Ses klonlama için referans (6-20 sn WAV).
            language: Dil kodu (self.settings.supported_languages).
            output_path: Çıktı yolu.
        
        Returns:
            Path: Üretilen WAV dosyası.
        
        Raises:
            SynthesisError: Sentezleme sırasında hata.
            SpeakerFileError: Geçersiz speaker dosyası.
        """
        if not output_path:
            output_path = self.settings.output_dir / f'synth_{language[:2]}_{Path(text[:20]).stem}.wav'
        
        if speaker_wav and not speaker_wav.exists():
            raise SpeakerFileError(f'Speaker dosyası bulunamadı: {speaker_wav}')
        
        kwargs: dict = {'language': language}
        if speaker_wav:
            kwargs['speaker_wav'] = str(speaker_wav)
            logger.info(f'Ses klonlama aktif: {speaker_wav.name}')
        
        try:
            self.tts.tts_to_file(text=text, file_path=str(output_path), **kwargs)
            logger.info(f'Sentezleme tamamlandı: {output_path.name} ({len(text)} karakter)')
            return output_path
        except Exception as e:
            logger.error(f'Sentezleme hatası: {e}')
            raise SynthesisError(f'Ses sentezleme başarıslandı: {str(e)}', e)
