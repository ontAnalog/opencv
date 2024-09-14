import cv2
import time
from pymavlink import mavutil

# Inisialisasi koneksi MAVLink ke Pixhawk
connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)
connection.wait_heartbeat()

# Fungsi untuk mengirim perintah kontrol gerak ke drone
def send_movement_command(roll, pitch, throttle, yaw):
    # Membuat pesan MAVLink untuk mengirim perintah kontrol
    connection.mav.manual_control_send(
        connection.target_system,  # Sistem ID (biasanya drone)
        roll,     # Roll (kanan/kiri)
        pitch,    # Pitch (maju/mundur)
        throttle, # Throttle (naik/turun)
        yaw,      # Yaw (rotasi)
        0         # Kode tombol (tidak digunakan)
    )

# Fungsi untuk menurunkan drone (landing)
def land_drone():
    # Kirim perintah untuk mode pendaratan
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0, 0, 0, 0,  # Param tidak digunakan
        0, 0, 0      # Koordinat pendaratan (gunakan posisi saat ini)
    )
    print("Drone sedang mendarat...")

# Inisialisasi kamera untuk deteksi objek
cap = cv2.VideoCapture(0)

# Parameter frame kamera
frame_width = 640
frame_height = 480
center_x = frame_width // 2
center_y = frame_height // 2
tolerance = 50  # Toleransi posisi objek dari tengah frame

# Deteksi objek menggunakan OpenCV (misalnya deteksi warna merah)
def detect_object(frame):
    # Ubah ke HSV untuk deteksi warna
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definisikan rentang warna untuk objek yang akan dideteksi (misal merah)
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)

    # Masker untuk warna merah
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    
    # Cari kontur pada area yang sesuai dengan mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        # Cari kontur dengan area terbesar
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return (x + w // 2, y + h // 2, w * h)  # Kembalikan posisi tengah objek dan luasnya
    
    return None

# Fungsi untuk memposisikan drone agar objek berada di tengah frame
def align_drone_to_object(obj_x, obj_y, frame_width, frame_height):
    error_x = obj_x - center_x
    error_y = obj_y - center_y

    if abs(error_x) > tolerance:
        # Geser drone ke kanan/kiri berdasarkan error X
        if error_x > 0:
            send_movement_command(-500, 0, 0, 300)  # Yaw ke kanan
        else:
            send_movement_command(5001, 0, 0, -300)  # Yaw ke kiri

    if abs(error_y) > tolerance:
        # Naikkan atau turunkan drone berdasarkan error Y
        if error_y > 0:
            send_movement_command(0, 0, -300, 0)  # Turun
        else:
            send_movement_command(0, 0, 300, 0)  # Naik

# Main loop
try:
    while True:
        # Baca frame dari kamera
        ret, frame = cap.read()
        if not ret:
            continue

        # Deteksi objek pada frame
        object_position = detect_object(frame)
        if object_position:
            obj_x, obj_y, obj_area = object_position

            # Tampilkan informasi di frame
            cv2.circle(frame, (obj_x, obj_y), 5, (255, 0, 0), -1)

            # Posisikan drone agar objek berada di tengah frame
            align_drone_to_object(obj_x, obj_y, frame_width, frame_height)

            # Jika objek besar (berarti drone cukup dekat), lakukan pendaratan
            if obj_area > 30000:  # Threshold untuk ukuran objek
                land_drone()
                break

        # Tampilkan frame dengan deteksi objek
        cv2.imshow("Object Detection", frame)

        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    # Bersihkan dan tutup
    cap.release()
    cv2.destroyAllWindows()
    connection.close()
