import cv2
import numpy as np
import serial
import time

# Setup komunikasi serial dengan Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Sesuaikan port sesuai dengan port USB Anda
time.sleep(2)  # Tunggu Arduino siap

# Fungsi untuk mendeteksi warna BGR tertentu
def detect_color(frame):
    # Definisikan rentang warna yang ingin dideteksi (BGR)
    lower_color = np.array([4, 45, 134])
    upper_color = np.array([5, 62, 184])

    # Cari warna dalam frame
    mask = cv2.inRange(frame, lower_color, upper_color)
    
    # Jika warna ditemukan, maka mask akan memiliki nilai non-zero
    if cv2.countNonZero(mask) > 0:
        return True
    return False

# Buka kamera atau video
cap = cv2.VideoCapture(1)  # Ganti dengan file video jika ingin mendeteksi dari video

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Deteksi warna pada frame
        if detect_color(frame):
            print("Warna terdeteksi, kirim sinyal ke Arduino.")
            arduino.write(b'1')  # Kirim sinyal ke Arduino
        else:
            print("Warna tidak terdeteksi.")
            arduino.write(b'0')  # Kirim sinyal '0' jika warna tidak terdeteksi
        
        # Tampilkan frame di jendela
        cv2.imshow('Frame', frame)
        
        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
