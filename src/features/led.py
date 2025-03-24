import time
from rpi_ws281x import PixelStrip, Color
from src.features.global_variables import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL

class LEDController:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.led_on = False
    
    def color_wipe(self, color, wait_ms=50):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def enable_led(self, color):
        try:
            if not self.led_on:
                print("Enabling LEDs...")
                self.color_wipe(color)
                self.led_on = True
            else:
                print("Disabling LEDs...")
                self.disable_led()
                self.led_on = False
        except KeyboardInterrupt:
            self.disable_led()
    
    def disable_led(self):
        print("Disabling LEDs...")
        self.color_wipe(Color(0, 0, 0))  # Turn off all LEDs
        self.led_on = False
