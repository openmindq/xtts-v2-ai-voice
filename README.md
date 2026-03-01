# XTTS-v2 AI Voice Generator

Profesyonel **metinden konuşmaya (TTS)** ve **ses klonlama (Voice Cloning)** aracı. Coqui XTTS-v2 modelini kullanarak NVIDIA GPU optimize edilmiş, CPU fallback destekli yüksek kaliteli ses üretimi.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![GPU](https://img.shields.io/badge/GPU-Optimized-green.svg)](https://pytorch.org/)

## Özellikler
- ✅ **Ses Klonlama:** 6-10 saniyelik WAV ile zero-shot voice cloning.
- ✅ **Çoklu Dil:** Türkçe (tr), İngilizce (en), İspanyolca (es) ve 10+ dil daha.
- ✅ **GPU/CPU:** Otomatik cihaz algılama (NVIDIA CUDA öncelikli).
- ✅ **CLI Arayüz:** Kolay komut satırı kullanımı.
- ✅ **Yüksek Kalite:** XTTS-v2 ile doğal ses sentezi.

## Kurulum
```bash
git clone https://github.com/openmindq/xtts-v2-ai-voice.git
cd xtts-v2-ai-voice
pip install -r requirements.txt
```

**Donanım:** NVIDIA GPU (4GB+ VRAM önerilir). CPU'da yavaş çalışır (i5-12400F uyumlu).

## Kullanım
### Temel TTS
```bash
python main.py --text \"Merhaba, bu bir test sesidir.\"
```

### Ses Klonlama
```bash
python main.py --text \"Ben klonlanmış bir sesim.\" --speaker samples/reference.wav --lang tr
```

### Parametreler
- `--text`: Zorunlu, sentezlenecek metin.
- `--speaker`: Opsiyonel, WAV ses örneği (samples/ dizinine koyun).
- `--lang`: Dil (tr varsayılan).
- `--output`: Çıktı dosyası (outputs/ dizinine kaydedilir).

## Örnekler
`samples/` dizinine 6-10 sn'lik temiz WAV koyun. `outputs/` sentezlenmiş sesleri içerir.

## Geliştirme
```bash
pytest tests/  # Testleri çalıştırın
```

## Uyarılar
- İlk çalıştırmada model (~2GB) indirilir.
- GPU yoksa CPU yavaş olur.

**Repo:** https://github.com/openmindq/xtts-v2-ai-voice
