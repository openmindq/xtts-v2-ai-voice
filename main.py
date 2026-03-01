#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from tts_engine import TTSEngine
from config import Config

def parse_args():
    parser = argparse.ArgumentParser(description='XTTS-v2 ile metinden konuşmaya ve ses klonlama.')
    parser.add_argument('--text', type=str, required=True, help='Sentezlenecek metin.')
    parser.add_argument('--speaker', type=Path, help='Ses klonlama için WAV dosyası (6-10 sn).')
    parser.add_argument('--lang', type=str, default='tr', choices=Config.SUPPORTED_LANGUAGES, help='Dil (varsayılan: tr).')
    parser.add_argument('--output', type=Path, help='Çıktı WAV dosyası.')
    return parser.parse_args()

def main():
    args = parse_args()
    engine = TTSEngine()
    output = engine.synthesize(
        text=args.text,
        speaker_wav=args.speaker,
        language=args.lang,
        output_path=args.output
    )
    print(f'✅ Ses dosyası hazır: {output}')

if __name__ == '__main__':
    main()
