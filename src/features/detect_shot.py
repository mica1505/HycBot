import RPi.GPIO as GPIO
from src.features import InfraLib
from src.features.global_variables import IR_RECEIVER


class ShotDetector:

    def __init__(self):
        GPIO.setup(IR_RECEIVER, GPIO.IN)

    def detect_shot(self):
        try:    
            while True:
                received = InfraLib.getSignal(IR_RECEIVER)
                if received:
                    print(received)
                   
        except KeyboardInterrupt:
            print("❌ Stopping program.")
            GPIO.cleanup()
        finally:
            GPIO.cleanup()
