MOTOR_PINS = {
    'A': {'pin1': 8, 'pin2': 10},
    'B': {'pin1': 13, 'pin2': 12}
}

# LED strip configuration:
LED_COUNT = 16        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 255  # Brightness (0-255)
LED_INVERT = False    # True to invert the signal
LED_CHANNEL = 0       # Set to '1' for GPIOs 13, 19, 41, 45, or 53