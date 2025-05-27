import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO

# ========================== LOAD MODEL YOLO ========================== #
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# ========================= KONFIGURASI ========================= #
CLASS_LABELS = {
    0: "Blast",
    1: "Hama Putih Palsu",
    2: "Hawar Daun Bakteri",
    3: "Stem Borer"
}

# ========================= FUNGSI DETEKSI ========================= #
def detect_pest_disease(image, conf_threshold=0.5, show_bbox=True):
    # Konversi gambar PIL ke OpenCV (RGB ke BGR)
    image = image.convert("RGB")
    image = image.resize((640, 640))
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    original_img = img.copy()

    # Jalankan deteksi dengan YOLOv11
    results = model(img)

    # Inisialisasi hasil deteksi
    detections = []

    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])  # Confidence score
            if conf < conf_threshold:
                continue  # Lewati jika confidence di bawah threshold
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            class_id = int(box.cls[0])  
            label = CLASS_LABELS.get(class_id, "Unknown")
            confidence = f"{conf * 100:.2f}%"  # Ubah ke format persentase
            
            # Simpan hasil confidence score
            detections.append({"Label": label, "Confidence": confidence})

            # Gambar bounding box jika diaktifkan
            if show_bbox:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(img, f"{label} ({confidence})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), detections

# ========================= STREAMLIT UI ========================= #
st.title("🌾Deteksi Hama & Penyakit Padi")
st.write("Upload gambar tanaman padi untuk mendeteksi hama dan penyakit secara otomatis.")

# Upload gambar
uploaded_file = st.file_uploader("📤 Unggah Gambar", type=["jpg", "png", "jpeg"])

# Pilih threshold confidence
conf_threshold = st.slider(
    "🎯 Ambang Confidence (tingkat keyakinan model dalam menampilkan deteksi)", 
    0.0, 1.0, 0.5, 0.05
)

# Penjelasan threshold confidence
with st.expander("ℹ️ Penjelasan Ambang Confidence"):
    st.markdown("""
    Ambang confidence menentukan seberapa yakin model harus merasa sebelum menampilkan hasil deteksi.

    - **Nilai rendah (misal 0.3)**: Model akan menampilkan lebih banyak hasil, tetapi bisa termasuk deteksi yang tidak akurat.
    - **Nilai tinggi (misal 0.7)**: Hanya hasil yang benar-benar diyakini yang akan ditampilkan, tapi bisa melewatkan beberapa deteksi.

    💡 **Rekomendasi**: Gunakan nilai antara **0.4 hingga 0.6** untuk hasil yang seimbang.
    """)


# Opsi bounding box
show_bbox = st.checkbox("🖼️ Tampilkan Bounding Box", value=True)

if uploaded_file is not None:
    # Tampilkan gambar asli
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Gambar yang Diunggah", use_container_width=True)

    # Jalankan deteksi saat tombol ditekan
    if st.button("🔍 Deteksi"):
        detected_img, detections = detect_pest_disease(image, conf_threshold, show_bbox)
        
        # Tampilkan hasil deteksi
        st.image(detected_img, caption="✅ Hasil Deteksi", use_container_width=True)
        
        # **Tampilkan confidence score dalam tabel**
        st.subheader("📊 Hasil Deteksi")
        if detections:
            df = pd.DataFrame(detections)
            df.index = df.index + 1
            df.index.name = "No"
            st.table(df)
        else:
            st.write("❌ Tidak ada objek terdeteksi dengan threshold ini.")
        
        # Simpan hasil deteksi
        output_path = "detected_image.jpg"
        cv2.imwrite(output_path, cv2.cvtColor(detected_img, cv2.COLOR_RGB2BGR))
        
        # Tombol untuk mengunduh gambar hasil deteksi
        with open(output_path, "rb") as file:
            st.download_button(label="📥 Unduh Hasil Deteksi",
                               data=file,
                               file_name="deteksi_padi.jpg",
                               mime="image/jpeg")