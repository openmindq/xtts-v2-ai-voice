#!/usr/bin/env python3
\"\"\"CLI arayüzü XTTS Voice için.\"\"\"
import argparse
import sys
import logging
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from xtts_voice.tts_engine import TTSEngine
from xtts_voice.settings import get_settings
from xtts_voice.exceptions import XTTSVoiceError

console = Console()
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Profesyonel XTTS-v2 TTS & Voice Cloning CLI.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Örnek: xtts-voice --text "Merhaba" --speaker samples/ref.wav --lang tr'
    )
    parser.add_argument('--text', type=str, help='Sentezlenecek metin.')
    parser.add_argument('--file', type=Path, help='Sentezlenecek metinleri içeren dosya (her satır bir cümle).')
    parser.add_argument('--speaker', type=Path, help='Ses klonlama WAV (6-20 sn).')
    parser.add_argument('--lang', type=str, default='tr', help='Dil (tr/en/es vb.).')
    parser.add_argument('--output', type=Path, help='Çıktı WAV yolu veya klasörü.')
    parser.add_argument('--verbose', action='store_true', help='Detaylı log.')
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    
    if not args.text and not args.file:
        console.print('[red]❌ Hata: --text veya --file belirtilmelidir.[/red]')
        sys.exit(1)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        engine = TTSEngine()
        
        texts = []
        if args.text:
            texts.append(args.text)
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        
        for i, text in enumerate(texts):
            output_file = args.output
            if output_file and output_file.is_dir():
                output_file = output_file / f'output_{i}.wav'
            
            with Progress(
                SpinnerColumn(),
                TextColumn('[progress.description]{task.description}'),
                console=console
            ) as progress:
                progress.add_task(f'Sentezleniyor ({i+1}/{len(texts)})...', total=None)
                output = engine.synthesize(
                    text=text,
                    speaker_wav=args.speaker,
                    language=args.lang,
                    output_path=output_file
                )
            
            console.print(f'[green]✅ Ses {i+1} hazır: {output}[/green]')
        
    except XTTSVoiceError as e:
        console.print(f'[red]❌ Hata: {e}[/red]')
        logger.error(f'XTTS hatası: {e}')
        sys.exit(1)
    except KeyboardInterrupt:
        console.print('[yellow]⚠️ İşlem iptal edildi.[/yellow]')
        sys.exit(130)
    except Exception as e:
        console.print(f'[red]Beklenmeyen hata: {e}[/red]')
        logger.critical(f'Kritik hata: {e}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
