import RPi.GPIO as GPIO
import time

from src.features.global_variables import SENSOR_LEFT, SENSOR_MIDDLE, SENSOR_RIGHT
# from src.server.client import notify_flag_zone

class SensorController:
    def __init__(self):
        self.SENSOR_LEFT = SENSOR_LEFT
        self.SENSOR_MIDDLE = SENSOR_MIDDLE
        self.SENSOR_RIGHT = SENSOR_RIGHT

        GPIO.setup(self.SENSOR_LEFT, GPIO.IN)
        GPIO.setup(self.SENSOR_MIDDLE, GPIO.IN)
        GPIO.setup(self.SENSOR_RIGHT, GPIO.IN)
        
        self.running = True  # Control flag for the thread
        self.res = None
    def read_sensors(self):
        """Read the state of the three sensors."""
        return {
            "Gauche": "blanc" if GPIO.input(self.SENSOR_LEFT) == 0 else "noir",
            "Milieu": "blanc" if GPIO.input(self.SENSOR_MIDDLE) == 0 else "noir",
            "Droite": "blanc" if GPIO.input(self.SENSOR_RIGHT) == 0 else "noir",
        }
    
    def detect_transition_zone(self):
        """Monitor sensor changes and detect transitions."""
        try:
            previous_states = self.read_sensors()
            print(previous_states)
            while self.running:
                current_states = self.read_sensors()
                for sensor in current_states.keys():
                    if current_states[sensor] != previous_states[sensor]:
                        self.res = f"🔄 Transition détectée sur {sensor}: {previous_states[sensor]} -> {current_states[sensor]}"
                        print(self.res)
                        # if res == "🔄 Transition détectée sur Gauche: noir -> blanc":
                        #     notify_flag_zone("ENTER_FLAG_AREA")
                        # elif res == "🔄 Transition détectée sur Gauche: blanc -> noir":
                        #     notify_flag_zone("EXIT_FLAG_AREA")
                    previous_states = current_states
                time.sleep(0.5)
        finally:
            GPIO.cleanup()
    
    def stop(self):
        self.running = False
