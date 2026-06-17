---
title: AI Fruit Classifier
emoji: 🍓
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---
# Fruit Classifier Web App

Aplikasi web berbasis AI untuk memenuhi tugas kuliah "Penerapan Convolutional Neural Networks (CNN) pada Aplikasi Berbasis Web Menggunakan Flask". Aplikasi ini dapat mendeteksi berbagai jenis buah menggunakan model Deep Learning.

## 🚀 Fitur Utama
- Upload gambar buah dan dapatkan hasil prediksi secara instan
- Model CNN yang dapat dilatih ulang
- Opsi menggunakan Transfer Learning (MobileNetV2)
- Tampilan UI yang modern dan responsif (Bootstrap 5)
- Drag & Drop untuk upload file dengan live preview

## 📁 Struktur Folder Project
```
fruit-classifier-web/
├── app.py                      # File utama Flask Web App
├── requirements.txt            # Daftar library yang dibutuhkan
├── README.md                   # Dokumentasi aplikasi
├── models/                     # Folder penyimpanan model AI (.h5) dan class_names.json
├── static/                     # Folder untuk aset statis web
│   ├── css/
│   │   └── style.css           # Styling kustom
│   ├── js/
│   │   └── main.js             # Script untuk UI interactions
│   └── uploads/                # Direktori penyimpanan sementara gambar upload
├── templates/                  # Folder HTML templates (Jinja2)
│   ├── base.html               # Layout dasar web
│   ├── index.html              # Halaman beranda / form upload
│   └── result.html             # Halaman hasil prediksi
└── training/                   # Folder untuk proses training model
    ├── train_model.py          # Script training CNN & MobileNetV2
    └── dataset/                # Folder dataset gambar
        ├── train/              # Dataset training
        └── validation/         # Dataset validasi
```

## 🛠️ Persiapan dan Instalasi
1. Pastikan Python 3.x sudah terinstall.
2. Clone repository atau ekstrak folder project ini.
3. Buka terminal/command prompt dan masuk ke folder project:
   ```bash
   cd fruit-classifier-web
   ```
4. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## 🧠 Cara Melatih Model (Training)
1. Pastikan dataset sudah berada di dalam folder `training/dataset/train` dan `training/dataset/validation`.
2. Buka terminal, masuk ke folder `training`:
   ```bash
   cd training
   ```
3. Jalankan script training:
   ```bash
   python train_model.py
   ```
4. Model akan dilatih dan otomatis tersimpan di folder `models/fruit_model.h5`. File `class_names.json` juga akan dihasilkan.

*Catatan: Jika ingin menggunakan MobileNetV2, ubah `USE_MOBILENET = True` pada baris ke-17 di dalam `train_model.py`.*

## 💻 Cara Menjalankan Aplikasi Web
1. Buka terminal, kembali ke direktori root (folder utama project).
2. Jalankan Flask app:
   ```bash
   python app.py
   ```
3. Buka browser dan akses alamat `http://localhost:5000` atau `http://127.0.0.1:5000`.

## 🌐 Cara Deploy ke Render
Render.com adalah platform gratis untuk hosting aplikasi web.
1. Buat akun di [Render.com](https://render.com/).
2. Push project ini ke GitHub repository Anda.
3. Di dashboard Render, pilih **New +** > **Web Service**.
4. Hubungkan dengan akun GitHub Anda dan pilih repository project ini.
5. Konfigurasi Deployment:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Klik **Create Web Service**. Tunggu beberapa menit hingga proses build selesai.
7. Aplikasi Anda siap diakses melalui URL yang diberikan oleh Render.
