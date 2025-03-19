import RPi.GPIO as GPIO
import time
import uuid
from src.features import InfraLib
from src.features import led
from rpi_ws281x import PixelStrip, Color
from src.features.led import enableLED,disableLED

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def send_shot():
    enableLED(Color(0, 255, 0))
    InfraLib.IRBlast(uuid.getnode(), "LASER")
    disableLED()
    print("🔹 Shot sent!")



