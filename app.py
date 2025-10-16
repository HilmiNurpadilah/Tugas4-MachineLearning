"""
Aplikasi Flask untuk Prediksi Suhu Menggunakan LSTM
Dibuat untuk TA-04 Machine Learning
"""

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import sys
# Fix numpy._core compatibility untuk load scaler
if not hasattr(np, '_core'):
    np._core = np.core
    sys.modules['numpy._core'] = np.core

import pandas as pd
from tensorflow.keras.models import load_model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import json
import os

app = Flask(__name__)

# Load model, scaler, dan info
MODEL_PATH = 'models/lstm_temperature_model.h5'
SCALER_PATH = 'models/scaler.save'
INFO_PATH = 'models/model_info.json'
DATA_PATH = 'data_for_app.csv'

print("Loading model dan scaler...")
# Rebuild model architecture untuk avoid Keras 3.x compatibility issues
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Rebuild exact architecture
model = Sequential([
    LSTM(100, return_sequences=True, input_shape=(60, 8)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dense(1)
])

# Load weights dari .h5 file
print(f"Loading weights from: {MODEL_PATH}")
try:
    model.load_weights(MODEL_PATH)
    print("✅ Model weights loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading weights: {e}")
    # Fallback: try load full model
    model = load_model(MODEL_PATH, compile=False)

# Compile model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Load scaler (numpy._core fix sudah di atas)
scaler = joblib.load(SCALER_PATH)

with open(INFO_PATH, 'r') as f:
    model_info = json.load(f)

timesteps = model_info['timesteps']
n_features = model_info['n_features']
fitur_model = model_info['fitur_model']

print(f"✅ Model loaded! Timesteps: {timesteps}, Features: {n_features}")

df = pd.read_csv(DATA_PATH, parse_dates=['date'], index_col='date')
print(f"✅ Data loaded! Shape: {df.shape}")


def create_plot_base64(fig):
    """Konversi matplotlib figure ke base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_b64


@app.route('/')
def index():
    """Halaman utama dengan visualisasi data historis"""
    
    data_plot = df.tail(5000)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data_plot.index, data_plot['suhu'], linewidth=0.5, color='red', alpha=0.8)
    ax.set_title('Suhu Historis (Data Terakhir)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Tanggal', fontsize=10)
    ax.set_ylabel('Suhu (°C)', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    hist_plot = create_plot_base64(fig)
    
    stats = {
        'total_data': len(df),
        'tanggal_awal': df.index.min().strftime('%Y-%m-%d %H:%M'),
        'tanggal_akhir': df.index.max().strftime('%Y-%m-%d %H:%M'),
        'suhu_min': f"{df['suhu'].min():.2f}",
        'suhu_max': f"{df['suhu'].max():.2f}",
        'suhu_rata': f"{df['suhu'].mean():.2f}",
        'test_rmse': f"{model_info['test_rmse']:.4f}",
        'test_mae': f"{model_info['test_mae']:.4f}",
        'test_r2': f"{model_info['test_r2']:.4f}"
    }
    
    return render_template('index.html', hist_plot=hist_plot, stats=stats)


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint untuk prediksi suhu"""
    
    try:
        last_data = df.tail(timesteps)[fitur_model].values
        last_data_scaled = scaler.transform(last_data)
        X_input = last_data_scaled.reshape(1, timesteps, n_features)
        
        pred_scaled = model.predict(X_input, verbose=0)[0][0]
        
        dummy = np.zeros((1, n_features))
        dummy[0, 0] = pred_scaled
        pred_actual = scaler.inverse_transform(dummy)[0, 0]
        
        suhu_terakhir = df['suhu'].iloc[-1]
        tanggal_terakhir = df.index[-1].strftime('%Y-%m-%d %H:%M')
        
        result = {
            'success': True,
            'prediksi_suhu': round(float(pred_actual), 2),
            'suhu_terakhir': round(float(suhu_terakhir), 2),
            'tanggal_terakhir': tanggal_terakhir,
            'selisih': round(float(pred_actual - suhu_terakhir), 2)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/predict_multiple', methods=['POST'])
def predict_multiple():
    """Prediksi beberapa timestep ke depan"""
    
    try:
        data = request.get_json()
        n_steps = int(data.get('n_steps', 10))
        
        predictions = []
        current_sequence = df.tail(timesteps)[fitur_model].values.copy()
        
        for i in range(n_steps):
            scaled_sequence = scaler.transform(current_sequence)
            X_input = scaled_sequence.reshape(1, timesteps, n_features)
            
            pred_scaled = model.predict(X_input, verbose=0)[0][0]
            
            dummy = np.zeros((1, n_features))
            dummy[0, 0] = pred_scaled
            pred_actual = scaler.inverse_transform(dummy)[0, 0]
            
            predictions.append(float(pred_actual))
            
            new_row = current_sequence[-1].copy()
            new_row[0] = pred_actual
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        return jsonify({
            'success': True,
            'predictions': [round(p, 2) for p in predictions],
            'n_steps': n_steps
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/stats')
def stats():
    """API untuk mendapatkan statistik data"""
    
    stats_data = {
        'total_records': int(len(df)),
        'date_range': {
            'start': df.index.min().strftime('%Y-%m-%d %H:%M'),
            'end': df.index.max().strftime('%Y-%m-%d %H:%M')
        },
        'temperature': {
            'min': float(df['suhu'].min()),
            'max': float(df['suhu'].max()),
            'mean': float(df['suhu'].mean()),
            'std': float(df['suhu'].std())
        },
        'model_performance': {
            'rmse': float(model_info['test_rmse']),
            'mae': float(model_info['test_mae']),
            'r2': float(model_info['test_r2'])
        }
    }
    
    return jsonify(stats_data)


if __name__ == '__main__':
    # Railway akan set PORT via environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
