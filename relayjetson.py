import Jetson.GPIO as GPIO
import time

# Set GPIO mode ke BOARD (berdasarkan nomor pin fisik)
GPIO.setmode(GPIO.BOARD)

# Definisikan pin GPIO yang digunakan untuk relay
relay_pin = 18  # Pin 18 adalah GPIO 24

# Set pin relay sebagai output
GPIO.setup(relay_pin, GPIO.OUT)

def relay_on():
    GPIO.output(relay_pin, GPIO.HIGH)  # Aktifkan relay (tergantung pada jenis relay)
    print("Relay ON")

def relay_off():
    GPIO.output(relay_pin, GPIO.LOW)  # Matikan relay
    print("Relay OFF")

try:
    while True:
        relay_on()   # Nyalakan relay
        time.sleep(5)  # Tunggu 5 detik
        relay_off()  # Matikan relay
        time.sleep(5)  # Tunggu 5 detik

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    # Pastikan GPIO bersih setelah selesai digunakan
    GPIO.cleanup()

# Install GPIO jika belum diinstall:
#   sudo apt-get install python3-pip
#   pip3 install Jetson.GPIO
