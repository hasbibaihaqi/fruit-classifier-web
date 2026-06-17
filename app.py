import os
import json
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model

app = Flask(__name__)

# ==========================================
# Konfigurasi Aplikasi
# ==========================================
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Max 16MB

# Pastikan folder upload tersedia
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# Load Model & Class Names
# ==========================================
MODEL_PATH = 'models/fruit_model.h5'
CLASS_NAMES_PATH = 'models/class_names.json'

model = None
class_names = []

try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print("Model CNN berhasil dimuat.")
    else:
        print(f"Warning: Model tidak ditemukan di {MODEL_PATH}")
        
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
        print(f"Berhasil memuat {len(class_names)} kelas.")
    else:
        print(f"Warning: File class_names.json tidak ditemukan di {CLASS_NAMES_PATH}")
        # Default jika belum ada (sesuai dataset train jika belum di run train_model.py)
        class_names = ['apple', 'banana', 'orange', 'rottenapples', 'rottenbanana', 'rottenoranges'] 
except Exception as e:
    print(f"Error saat inisialisasi: {e}")

# ==========================================
# Helper Functions
# ==========================================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(filepath):
    """
    Preprocessing gambar sebelum diprediksi oleh model.
    """
    # Membaca gambar menggunakan OpenCV
    img = cv2.imread(filepath)
    # Konversi BGR (OpenCV default) ke RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Resize ke ukuran yang diharapkan model (150x150)
    img = cv2.resize(img, (150, 150))
    # Normalisasi (0-1)
    img = img / 255.0
    # Expand dimensi untuk batch (1, 150, 150, 3)
    img = np.expand_dims(img, axis=0)
    return img

# ==========================================
# Routes
# ==========================================
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('index.html', error="Model AI belum tersedia. Silakan jalankan training terlebih dahulu.")
        
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Preprocessing dan Prediksi
            img_array = prepare_image(filepath)
            predictions = model.predict(img_array)
            
            # Model kita menggunakan softmax di akhir, jadi output sudah berupa probabilitas
            score = predictions[0]
            class_index = np.argmax(score)
            
            if class_index < len(class_names):
                predicted_class = class_names[class_index]
            else:
                predicted_class = "Unknown"
                
            confidence = float(np.max(score)) * 100
            
            # Render ke halaman result
            return render_template('result.html', 
                                   image_path=f"uploads/{filename}", 
                                   prediction=predicted_class, 
                                   confidence=f"{confidence:.2f}")
                                   
        except Exception as e:
            print(f"Error saat prediksi: {e}")
            return render_template('index.html', error="Terjadi kesalahan pada saat memproses gambar.")
            
    return render_template('index.html', error="Format file tidak didukung. Gunakan PNG, JPG, atau JPEG.")

if __name__ == '__main__':
    # Gunakan host 0.0.0.0 agar bisa diakses secara eksternal jika di-deploy
    app.run(debug=True, host='0.0.0.0', port=5000)