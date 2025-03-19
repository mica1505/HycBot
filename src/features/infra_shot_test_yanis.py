import RPi.GPIO as GPIO
import uuid
from src.features import InfraLib
from rpi_ws281x import Color
from src.features import InfraLib
from rpi_ws281x import PixelStrip, Color
from src.features.led import enableLED,disableLED

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
IR_RECEIVER = 15
GPIO.setup(IR_RECEIVER, GPIO.IN)

def receive_shot():
    enableLED(Color(255, 0, 0))
    InfraLib.IRBlast(uuid.getnode(), "LASER")
    disableLED()
    print("🔹 Shot sent!")
try: 
    while True:
        shooter_value = InfraLib.getSignal(IR_RECEIVER)
        print(shooter_value)
        if shooter_value:
            receive_shot( )
except KeyboardInterrupt:
    print("❌ Stopping program.")
    GPIO.cleanup()
finally:
    GPIO.cleanup()

