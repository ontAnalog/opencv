import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Inisialisasi I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inisialisasi PCA9685
pca = PCA9685(i2c)
pca.frequency = 50  # Set frekuensi PWM untuk servo (50 Hz biasanya untuk servo)

# Inisialisasi servo pada kanal 0 PCA9685
servo0 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)

# Fungsi untuk menggerakkan servo ke sudut tertentu
def move_servo(angle):
    servo0.angle = angle
    print(f"Servo bergerak ke sudut {angle} derajat")

# Contoh gerakan servo
try:
    while True:
        move_servo(0)    # Gerakkan ke sudut 0 derajat
        time.sleep(2)    # Tunggu 2 detik
        
        move_servo(90)   # Gerakkan ke sudut 90 derajat
        time.sleep(2)
        
        move_servo(180)  # Gerakkan ke sudut 180 derajat
        time.sleep(2)

except KeyboardInterrupt:
    print("Program dihentikan")

# Matikan semua kanal setelah selesai
pca.deinit()

# Install dependensi dan library:  
#    sudo apt update
#    sudo apt install python3-pip
#    pip3 install adafruit-circuitpython-pca9685
