import RPi.GPIO as GPIO
from src.features.global_variables import MOTOR_PINS

class MotorController:
    def __init__(self):
        for motor in MOTOR_PINS.values():
            GPIO.setup(motor['pin1'], GPIO.OUT)
            GPIO.setup(motor['pin2'], GPIO.OUT)
        
    def move(self, direction):
        try:
            if direction == 'right':
                GPIO.output(MOTOR_PINS['A']['pin1'], True)
                GPIO.output(MOTOR_PINS['A']['pin2'], False)
                GPIO.output(MOTOR_PINS['B']['pin1'], True)
                GPIO.output(MOTOR_PINS['B']['pin2'], False)
            elif direction == 'left':
                GPIO.output(MOTOR_PINS['A']['pin1'], False)
                GPIO.output(MOTOR_PINS['A']['pin2'], True)
                GPIO.output(MOTOR_PINS['B']['pin1'], False)
                GPIO.output(MOTOR_PINS['B']['pin2'], True)
            elif direction == 'backward':
                GPIO.output(MOTOR_PINS['A']['pin1'], False)
                GPIO.output(MOTOR_PINS['A']['pin2'], True)
                GPIO.output(MOTOR_PINS['B']['pin1'], True)
                GPIO.output(MOTOR_PINS['B']['pin2'], False)
            elif direction == 'forward':
                GPIO.output(MOTOR_PINS['A']['pin1'], True)
                GPIO.output(MOTOR_PINS['A']['pin2'], False)
                GPIO.output(MOTOR_PINS['B']['pin1'], False)
                GPIO.output(MOTOR_PINS['B']['pin2'], True)
            else:
                self.stop()
        except Exception as e:
            print(f"Error in move function: {e}")
    
    def stop(self):
        try:
            for motor in MOTOR_PINS.values():
                GPIO.output(motor['pin1'], False)
                GPIO.output(motor['pin2'], False)
        except Exception as e:
            print(f"Error in stop function: {e}")
    
    def cleanup(self):
        GPIO.cleanup()