# 🎙️ XTTS-v2 Production API & CLI

**Üretim seviyesinde, yüksek performanslı metinden konuşmaya (TTS) ve ses klonlama mikroservisi.** 

## ⚡ Temel Özellikler
- **Gerçek Zamanlı Streaming:** Düşük gecikme (latency) ile anında ses akışı (TTFB < 500ms).
- **Yüksek Performans:** FP16 hassasiyeti ve GPU bellek yönetimi (CUDA 12.1+).
- **Akıllı Önbellek (Caching):** MD5 tabanlı disk/bellek cache mekanizması.
- **Dinamik Model Yönetimi:** Singleton mimari, model warmup ve iş parçacığı güvenliği.
- **Docker Ready:** NVIDIA GPU destekli konteynır yapısı hazır.

## 🐳 Docker ile Hızlı Başlat
```bash
# GPU destekli Docker konteynırını ayağa kaldırın
docker-compose up -d --build
```
*API http://localhost:8000 adresinden erişilebilir olacaktır.*

## 🚀 Yerel Kurulum
```bash
git clone https://github.com/openmindq/xtts-v2-ai-voice
cd xtts-v2-ai-voice
pip install -e .
```

## 💻 Kullanım
### API Endpoints
- **POST `/stream`**: `{"text": "Merhaba", "language": "tr", "speaker_wav": "samples/ref.wav"}` -> Streaming Ses Akışı (WAV Chunklar).
- **POST `/synthesize`**: `{"text": "...", "use_cache": true}` -> Tam Ses Dosyası (Cache destekli).
- **GET `/health`**: GPU ve Model durumunu kontrol eder.

### CLI (Yerel Kullanım)
```bash
# Tek metin
xtts-voice --text "Bu klonlanmış sesim." --speaker samples/ref.wav --lang tr --output output.wav

# Toplu metin işleme (dosyadan)
xtts-voice --file texts.txt --speaker samples/ref.wav --output output_dir/
```

## 🛠 Mimari Yapı
- `src/xtts_voice/core/`: Optimize edilmiş motor ve model yönetimi.
- `src/xtts_voice/api/`: FastAPI tabanlı yüksek performanslı endpoint'ler.
- `src/xtts_voice/utils/`: Caching ve loglama araçları.

**Gereksinimler:** NVIDIA RTX 30xx+ (6GB+ VRAM önerilir), CUDA 11.8/12.1+, 16GB RAM.
