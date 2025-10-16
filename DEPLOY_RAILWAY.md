# 🚂 Panduan Deploy ke Railway

## 📋 Langkah 1: Push ke GitHub

Jalankan command berikut di terminal (PowerShell) satu per satu:

```powershell
# 1. Masuk ke folder project
cd "C:\Users\hilmi\Documents\SEMESTER 5\Prak machine learning\Prak 4\TA-04"

# 2. Git add (sudah dilakukan)
git add .

# 3. Commit (jalankan ini)
git commit -m "Initial commit"

# 4. Set branch ke main
git branch -M main

# 5. Push ke GitHub
git push -u origin main
```

**Jika ada conflict/error saat push:**
```powershell
# Force push (hati-hati, ini akan overwrite remote)
git push -u origin main --force
```

---

## 🚂 Langkah 2: Deploy ke Railway

### A. Sign Up / Login Railway

1. Buka https://railway.app
2. Klik **Login with GitHub**
3. Authorize Railway untuk akses repository

### B. Create New Project

1. Di Railway Dashboard, klik **New Project**
2. Pilih **Deploy from GitHub repo**
3. Cari dan pilih repository: `HilmiNurpadilah/Tugas4-MachineLearning`
4. Klik repository tersebut

### C. Configure Deployment

Railway akan **auto-detect** bahwa ini adalah Python app dan akan:
- Otomatis membaca `requirements.txt`
- Otomatis membaca `Procfile`
- Otomatis membaca `runtime.txt`

**Tidak perlu konfigurasi tambahan!** Railway sangat smart.

### D. Wait for Build

1. Railway akan mulai build otomatis
2. Tunggu 3-5 menit untuk proses build
3. Monitor logs di tab **Deployments**

### E. Generate Domain

1. Setelah build sukses, klik tab **Settings**
2. Scroll ke bagian **Networking**
3. Klik **Generate Domain**
4. Railway akan memberikan URL seperti: `https://tugas4-machinelearning-production.up.railway.app`

### F. Test Aplikasi

1. Klik URL yang diberikan
2. Aplikasi Flask Anda seharusnya sudah live! 🎉
3. Test semua fitur prediksi

---

## 🔧 Troubleshooting

### Error: "Application failed to start"

**Solusi:**
1. Check logs di Railway Dashboard
2. Pastikan `Procfile` benar:
   ```
   web: gunicorn app:app
   ```
3. Pastikan `requirements.txt` lengkap
4. Pastikan `runtime.txt` ada:
   ```
   python-3.10.12
   ```

### Error: "Module not found"

**Solusi:**
1. Pastikan library ada di `requirements.txt`
2. Rebuild project:
   - Settings → Redeploy

### Error: "Model file not found"

**Solusi:**
1. Pastikan folder `models/` dan filenya ter-push ke GitHub
2. Check `.gitignore` tidak block file `.h5`

### Error: "Port already in use"

**Solusi:**
Railway otomatis set PORT, pastikan di `app.py`:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

## ⚙️ Konfigurasi Tambahan (Opsional)

### Environment Variables

Jika perlu set environment variables:
1. Railway Dashboard → **Variables**
2. Add variable:
   - Key: `FLASK_ENV`
   - Value: `production`

### Custom Domain

Jika punya domain sendiri:
1. Settings → **Networking** → **Custom Domain**
2. Tambahkan domain Anda
3. Update DNS settings sesuai instruksi Railway

---

## 📊 Monitoring

Railway menyediakan:
- **Metrics:** CPU, Memory, Network usage
- **Logs:** Real-time application logs
- **Deployments:** History semua deployment

---

## 💰 Pricing

**Free Tier Railway:**
- $5 credit per month (gratis)
- Cukup untuk project kecil
- Sleep setelah inactive (cold start ~10-20 detik)

**Jika habis:**
- Upgrade ke Hobby plan ($5/month)
- Atau gunakan Render (gratis unlimited)

---

## 🎯 Checklist Deploy

- [ ] Push code ke GitHub berhasil
- [ ] Railway project dibuat
- [ ] Build sukses (check logs)
- [ ] Domain di-generate
- [ ] Aplikasi bisa diakses
- [ ] Test semua fitur prediksi
- [ ] Screenshot untuk laporan
- [ ] Update README.md dengan URL deployment

---

## 📝 Update README dengan URL

Setelah deploy, update `README.md`:

```markdown
## 🌐 Live Demo

Aplikasi dapat diakses di: **https://tugas4-machinelearning-production.up.railway.app**
```

Lalu commit dan push:
```bash
git add README.md
git commit -m "Add deployment URL"
git push
```

---

## 🔄 Re-deploy Setelah Update Code

Setelah update code:
```bash
git add .
git commit -m "Update: [deskripsi perubahan]"
git push
```

Railway akan **auto-deploy** otomatis setelah push ke GitHub! 🚀

---

## ✅ Selesai!

Aplikasi Anda sekarang online dan bisa diakses dari mana saja!

**URL Deployment:** `https://[your-app].up.railway.app`

**Good luck! 🎉**
