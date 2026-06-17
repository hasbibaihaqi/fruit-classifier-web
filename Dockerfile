# Gunakan image Python ringan
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies untuk OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh file proyek
COPY . .

# Buat direktori uploads dan beri izin (karena HF spaces read-only secara default kecuali di folder tertentu)
RUN mkdir -p static/uploads && chmod -R 777 static/uploads

# Expose port (HF Spaces default port is 7860)
EXPOSE 7860

# Jalankan aplikasi menggunakan gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:app"]
