# XTTS-v2 AI Voice Generator ![Tests](https://github.com/openmindq/xtts-v2-ai-voice/workflows/CI/badge.svg) ![PyPI](https://img.shields.io/pypi/v/xtts-voice.svg)

**Profesyonel metinden konuşmaya (TTS) & ses klonlama aracı.** NVIDIA GPU optimize, CPU fallback, Pydantic konfig, Rich CLI.

## 🚀 Hızlı Kurulum
```bash
git clone https://github.com/openmindq/xtts-v2-ai-voice
cd xtts-v2-ai-voice
pip install -e .[dev]
```

## 📦 Paket Olarak Kur
```bash
pip install git+https://github.com/openmindq/xtts-v2-ai-voice.git
xtts-voice --text \"Merhaba Dünya\"
```

## 💻 Kullanım
```
xtts-voice --text \"Bu klonlanmış sesim.\" --speaker samples/ref.wav --lang tr --output output.wav --verbose
```

## 🛠 Geliştirme
```bash
black .
mypy src/
pytest --cov=src/xtts_voice --cov-report=html
```

## 🔧 Özellikler
- **GPU Otomatik:** CUDA varsa NVIDIA GPU kullanır.
- **Ses Klonlama:** 6-20 sn WAV ile zero-shot.
- **16+ Dil:** tr, en, es, fr...
- **Rich CLI:** Progress bar, renkli çıktı.
- **Production Ready:** Exceptions, logging, type hints, CI.

**Donanım:** NVIDIA RTX 30xx+ (4GB VRAM), 16GB RAM önerilir.
