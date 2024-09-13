import cv2
from PIL import Image
from util import get_limits  # pastikan fungsi ini bekerja dengan benar

orange = [0, 127, 255]  # warna oranye dalam BGR colorspace
cap = cv2.VideoCapture(1)  # ganti indeks jika perlu

if not cap.isOpened():
    print("Tidak dapat membuka kamera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Tidak dapat menangkap frame")
        continue

    # Konversi frame ke HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Dapatkan batas bawah dan atas untuk warna oranye
    lowerLimit, upperLimit = get_limits(color=orange)  # pastikan fungsi ini benar

    # Buat mask berdasarkan warna
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    # Konversi mask ke gambar PIL untuk mendapatkan bbox
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Tampilkan koordinat objek
        text = f"({x1}, {y1}), ({x2}, {y2})"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (x1, y1 - 10), font, 0.5, (255, 255, 255), 2)

    # Tampilkan frame di jendela
    cv2.imshow('frame', frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup kamera dan jendela
cap.release()
cv2.destroyAllWindows()
