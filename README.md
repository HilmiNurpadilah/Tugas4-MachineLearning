# Prediksi Suhu dengan LSTM - TA-04

Proyek Machine Learning untuk memprediksi suhu menggunakan Long Short-Term Memory (LSTM) Neural Network.

## 🌐 Live Demo

**Aplikasi dapat diakses di:** [Deployment URL akan ditambahkan setelah deploy]

> 💡 Setelah deploy ke Railway, update link di atas dengan URL deployment Anda!

## 📋 Deskripsi

Aplikasi web ini menggunakan model LSTM untuk memprediksi suhu berdasarkan data historis cuaca. Model dilatih dengan data multivariate yang mencakup berbagai parameter cuaca seperti kelembaban, tekanan udara, kecepatan angin, curah hujan, dan radiasi matahari.

## 🎯 Tujuan

- Membangun pipeline lengkap untuk time series forecasting
- Implementasi LSTM untuk prediksi suhu
- Membuat aplikasi web interaktif untuk visualisasi dan prediksi
- Deploy model ke production

## 🏗️ Struktur Proyek

```
TA-04/
├── prediksi_cuaca_lstm.ipynb    # Notebook utama dengan EDA & training
├── app.py                        # Flask application
├── templates/
│   └── index.html               # Frontend web
├── static/
│   └── plots/                   # Folder untuk plot
├── models/
│   ├── lstm_temperature_model.h5   # Model terlatih
│   ├── scaler.save                 # MinMaxScaler
│   └── model_info.json             # Informasi model
├── cleaned_weather.csv          # Dataset cuaca
├── data_for_app.csv            # Data untuk aplikasi
├── requirements.txt            # Dependencies
├── Procfile                    # Untuk deployment
└── README.md                   # Dokumentasi ini
```

## 🚀 Instalasi & Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd TA-04
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

### 3. Aktivasi Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Jalankan Notebook

```bash
jupyter notebook prediksi_cuaca_lstm.ipynb
```

Jalankan semua cell untuk:
- Eksplorasi data
- Preprocessing
- Training model
- Evaluasi
- Menyimpan model dan scaler

### 6. Jalankan Flask App

```bash
python app.py
```

Buka browser dan akses: `http://localhost:5000`

## 📊 Dataset

Dataset berisi data cuaca dengan kolom:
- **suhu**: Suhu udara (°C) - Target variable
- **kelembaban_relatif**: Kelembaban relatif (%)
- **tekanan_udara**: Tekanan udara (hPa)
- **kecepatan_angin**: Kecepatan angin (m/s)
- **curah_hujan**: Curah hujan (mm)
- **radiasi_gelombang_pendek**: Radiasi matahari (W/m²)
- Dan fitur waktu: bulan, hari_dalam_tahun, dll.

## 🧠 Arsitektur Model

```
Model: LSTM Sequential
_________________________________________________________________
Layer (type)                Output Shape              Params
=================================================================
LSTM_1 (LSTM)              (None, 60, 100)           43,600
Dropout_1 (Dropout)        (None, 60, 100)           0
LSTM_2 (LSTM)              (None, 50)                30,200
Dropout_2 (Dropout)        (None, 50)                0
Dense_1 (Dense)            (None, 25)                1,275
Dense_2 (Dense)            (None, 1)                 26
=================================================================
Total params: 75,101
```

**Hyperparameters:**
- Timesteps: 60
- Features: 8 (multivariate)
- Optimizer: Adam
- Loss: MSE
- Batch size: 32
- Epochs: 100 (dengan early stopping)

## 📈 Performa Model

Model dievaluasi menggunakan:
- **RMSE (Root Mean Squared Error)**
- **MAE (Mean Absolute Error)**
- **R² Score**

Hasil evaluasi dapat dilihat di notebook dan aplikasi web.

## 🌐 Fitur Aplikasi Web

1. **Dashboard Statistik**: Menampilkan statistik data dan performa model
2. **Visualisasi Data Historis**: Grafik suhu sepanjang waktu
3. **Prediksi Single Step**: Prediksi suhu untuk timestep berikutnya
4. **Prediksi Multiple Steps**: Prediksi beberapa timestep ke depan (10, 50 steps)
5. **API Endpoints**: RESTful API untuk integrasi

## 🔌 API Endpoints

### 1. GET `/`
Halaman utama aplikasi

### 2. POST `/predict`
Prediksi suhu untuk timestep berikutnya

**Response:**
```json
{
  "success": true,
  "prediksi_suhu": 25.34,
  "suhu_terakhir": 24.89,
  "tanggal_terakhir": "2020-12-31 23:50",
  "selisih": 0.45
}
```

### 3. POST `/predict_multiple`
Prediksi beberapa timestep ke depan

**Request:**
```json
{
  "n_steps": 10
}
```

**Response:**
```json
{
  "success": true,
  "predictions": [25.34, 25.67, 25.89, ...],
  "n_steps": 10
}
```

### 4. GET `/stats`
Mendapatkan statistik data dan model

## 🚀 Deployment

### Deploy ke Render

1. Push code ke GitHub
2. Buat account di [Render](https://render.com)
3. Create New Web Service
4. Connect repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn app:app`
7. Deploy!

### Deploy ke Railway

1. Install Railway CLI atau gunakan web interface
2. Push code ke GitHub
3. Connect repository ke Railway
4. Railway akan auto-detect Flask app
5. Deploy!

### Deploy ke Heroku

```bash
heroku login
heroku create nama-app-anda
git push heroku main
heroku open
```

## 📝 Cara Menggunakan

1. **Training Model:**
   - Buka `prediksi_cuaca_lstm.ipynb`
   - Jalankan semua cell
   - Model akan tersimpan di folder `models/`

2. **Menjalankan Aplikasi:**
   ```bash
   python app.py
   ```

3. **Akses Web Interface:**
   - Buka browser: `http://localhost:5000`
   - Klik tombol prediksi untuk melihat hasil

4. **Eksperimen dengan Model:**
   - Ubah timesteps
   - Tambah/kurangi fitur
   - Modifikasi arsitektur LSTM
   - Tune hyperparameters

## 🔧 Troubleshooting

### Error: Model tidak ditemukan
```bash
# Pastikan sudah menjalankan notebook untuk training
jupyter notebook prediksi_cuaca_lstm.ipynb
```

### Error: Module not found
```bash
# Install ulang dependencies
pip install -r requirements.txt
```

### Error: Memory error saat training
```python
# Kurangi batch_size atau gunakan data lebih sedikit
batch_size = 16  # default: 32
```

## 📚 Referensi

- TensorFlow Documentation: https://www.tensorflow.org/
- LSTM Paper: Hochreiter & Schmidhuber (1997)
- Flask Documentation: https://flask.palletsprojects.com/
- Time Series Forecasting with LSTM

## 👤 Author

**Nama:** Hilmi Nurpadilah  
**NIM:** 301230004
**Mata Kuliah:** Praktikum Machine Learning  
**Tugas:** TA-04 - Prediksi Time Series dengan LSTM

## 📄 License

MIT License - Proyek ini dibuat untuk keperluan akademik.

---

**Happy Coding! 🚀**
