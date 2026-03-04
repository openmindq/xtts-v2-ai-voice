# 🎙️ XTTS-v2 Production API & CLI

**Üretim seviyesinde, yüksek performanslı metinden konuşmaya (TTS) ve ses klonlama mikroservisi.** 

## ⚡ Temel Özellikler
- **Gerçek Zamanlı Streaming:** Düşük gecikme (latency) ile anında ses akışı (TTFB < 500ms).
- **Yüksek Performans:** FP16 hassasiyeti ve GPU bellek yönetimi (CUDA 12.1+).
- **Akıllı Önbellek (Caching):** MD5 tabanlı disk/bellek cache mekanizması.
- **Dinamik Model Yönetimi:** Singleton mimari, model warmup ve iş parçacığı güvenliği.
- **Docker Ready:** NVIDIA GPU destekli konteynır yapısı hazır.

## 🐳 Docker ile Üretim Ortamı
```bash
# Servisi ayağa kaldır (API, Redis, Worker)
docker-compose up -d --build
```
*API http://localhost:8000, Metrikler (Prometheus) http://localhost:8000/metrics adresinden erişilebilir.*

## 🚀 Yerel Kurulum
```bash
git clone https://github.com/openmindq/xtts-v2-ai-voice
cd xtts-v2-ai-voice
pip install -e .
```

## 💻 Kullanım
### API Endpoints
- **POST `/stream`**: Gerçek zamanlı streaming.
- **POST `/synthesize`**: Cache destekli tam dosya sentezleme.
- **GET `/health`**: Servis ve GPU durumu.
- **GET `/metrics`**: Prometheus formatında sistem metrikleri.

### CLI (Yerel Kullanım)
```bash
# Tek metin
xtts-voice --text "Bu klonlanmış sesim." --speaker samples/ref.wav --lang tr --output output.wav

# Toplu metin işleme (dosyadan)
xtts-voice --file texts.txt --speaker samples/ref.wav --output output_dir/
```

## 🛠 Mimari Yapı
- `core/`: Optimize edilmiş motor ve model yönetimi (Singleton).
- `api/`: FastAPI tabanlı yüksek performanslı endpoint'ler.
- `utils/`: Caching ve loglama araçları.
- `worker/`: Celery/Redis tabanlı async görev kuyruğu.

**Gereksinimler:** NVIDIA RTX 30xx+ (6GB+ VRAM önerilir), CUDA 11.8/12.1+, 16GB RAM, Redis.
