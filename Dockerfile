# NVIDIA CUDA 12.1 tabanlı PyTorch imajı
FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları kopyala ve kur
COPY pyproject.toml .
COPY requirements.txt .
RUN pip install --no-cache-dir .

# Uygulama kodlarını kopyala
COPY . .

# Önbellek ve çıktı dizinlerini oluştur
RUN mkdir -p cache/audio samples outputs

# Port aç ve başlat
EXPOSE 8000
CMD ["uvicorn", "src.xtts_voice.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
