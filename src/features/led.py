import time
from rpi_ws281x import PixelStrip, Color
from src.features.global_variables import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL


# Initialize LED strip
strip = None

def setup():
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip

# Function to fill LEDs with a specific color
def colorWipe(color, wait_ms=50):
    strip = setup()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.01)

# Function to enable LEDs with a color cycle
def enableLED(color):
    print("Enabling LEDs...")
    try:
        colorWipe(color)  # Red 
    except KeyboardInterrupt:
        disableLED()

# Function to disable LEDs (turn them off)
def disableLED():
    print("Disabling LEDs...")
    colorWipe(Color(0, 0, 0))  # Turn off all LEDs
    
if __name__=="__main__":
    # enableLED(Color(255,0,0))
    disableLED()
