# Rice Plant Pests and Diseases Detection

Aplikasi berbasis web untuk mendeteksi hama dan penyakit pada tanaman padi secara otomatis menggunakan model YOLOv11s dan framework Streamlit.

## 📌 Deskripsi

Aplikasi ini dikembangkan untuk membantu petani, penyuluh pertanian, dan peneliti dalam melakukan identifikasi dini terhadap serangan organisme pengganggu tanaman (OPT) pada padi. Dengan mengunggah gambar daun atau bagian tanaman padi, sistem akan memproses dan menampilkan jenis hama atau penyakit yang terdeteksi beserta tingkat keyakinan (confidence score)-nya.

## 🚀 Fitur Utama

- Upload gambar tanaman padi secara langsung dari perangkat pengguna
- Deteksi otomatis 4 kelas target:
  - Hama Putih Palsu
  - Hawar Daun Bakteri
  - Blast
  - Penggerek Batang (Stem Borer)
- Pengaturan threshold confidence untuk filter prediksi
- Opsi untuk menampilkan/menyembunyikan bounding box
- Download hasil deteksi (gambar dengan anotasi)

## 🖼️ Tampilan Aplikasi

Aplikasi ini tersedia secara publik dan dapat diakses melalui:

🔗 [https://riceplant-pests-diseases-detection.streamlit.app/](https://riceplant-pests-diseases-detection.streamlit.app/)

## 🛠️ Teknologi yang Digunakan

- Python
- Streamlit
- OpenCV
- Pillow (PIL)
- Ultralytics YOLOv11s

## 📂 Struktur Proyek (Sederhana)

├── deteksi_padi.py # Main script Streamlit
├── requirements.txt # Daftar dependensi untuk pip
├── packages.txt # Dependensi sistem (untuk kebutuhan deploy Streamlit Cloud)
├── README.md # Deskripsi proyek ini
├── best.pt # File model YOLOv11 hasil training

## ✅ Cara Menjalankan Secara Lokal

1. Clone repository:
	```bash
	git clone https://github.com/cabbbbsss/riceplant-pests-diseases-detection
	cd riceplant-pests-diseases-detection

2. Buat virtual environment (opsional)
	```bash
	python -m venv venv
	source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies:
	```bash
	pip install -r requirements.txt

4. Jalankan aplikasi:
	```bash
	streamlit run deteksi_padi.py

## 📈 Dataset dan Model

Model YOLOv11 dilatih menggunakan gabungan data dari:
- Public dataset Roboflow
- Dokumentasi Balai Perlindungan Tanaman Pertanian Provinsi Gorontalo

Model terdiri dari 4 kelas dan telah dioptimalkan menggunakan hyperparameter tuning untuk mencapai akurasi terbaik.

## 📃 Lisensi

Proyek ini dikembangkan untuk tujuan penelitian akademik. Silakan hubungi pengembang untuk penggunaan lebih lanjut.

email: sbrinaslsbla@gmail.com