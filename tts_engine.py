import torch
import logging
from pathlib import Path
from TTS.api import TTS
from config import Config
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() and Config.USE_GPU else 'cpu'
        logger.info(f'Kullanılacak cihaz: {self.device}')
        
        self.tts = TTS(Config.MODEL_NAME, gpu=(self.device == 'cuda'))
        Config.init_dirs()
    
    def synthesize(
        self, 
        text: str, 
        speaker_wav: Optional[Path] = None, 
        language: str = 'tr',
        output_path: Optional[Path] = None
    ) -> Path:
        \"\"\"
        Metni sese dönüştürür. Ses klonlama için speaker_wav belirtin.
        
        Args:
            text: Sentezlenecek metin.
            speaker_wav: Ses klonlama için referans WAV dosyası (6-10 sn).
            language: Dil kodu (tr, en vb.).
            output_path: Çıktı dosya yolu.
        
        Returns:
            Üretilen ses dosyasının yolu.
        \"\"\"
        if not output_path:
            output_path = Config.OUTPUT_DIR / f'output_{language}_{len(text[:20])}chars.wav'
        
        kwargs = {'language': language}
        if speaker_wav and speaker_wav.exists():
            kwargs['speaker_wav'] = str(speaker_wav)
            logger.info(f'Ses klonlama: {speaker_wav}')
        else:
            logger.info('Standart ses kullanılıyor.')
        
        self.tts.tts_to_file(text=text, file_path=str(output_path), **kwargs)
        logger.info(f'Ses üretildi: {output_path}')
        return output_path
