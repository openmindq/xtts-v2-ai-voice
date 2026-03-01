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
    parser.add_argument('--text', type=str, required=True, help='Sentezlenecek metin.')
    parser.add_argument('--speaker', type=Path, help='Ses klonlama WAV (6-20 sn).')
    parser.add_argument('--lang', type=str, default='tr', help='Dil (tr/en/es vb.).')
    parser.add_argument('--output', type=Path, help='Çıktı WAV yolu.')
    parser.add_argument('--verbose', action='store_true', help='Detaylı log.')
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        settings = get_settings()
        engine = TTSEngine()
        
        with Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}'),
            console=console
        ) as progress:
            task = progress.add_task('Sentezleme...', total=None)
            output = engine.synthesize(
                text=args.text,
                speaker_wav=args.speaker,
                language=args.lang,
                output_path=args.output
            )
            progress.update(task, description='Tamamlandı!')
        
        console.print(f'[green]✅ Ses hazır: {output}[/green]')
        console.print(f'[blue]📁 Boyut: {output.stat().st_size / 1024:.1f} KB[/blue]')
        
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
