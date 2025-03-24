import RPi.GPIO as GPIO
import socket
import time
from rpi_ws281x import Color

from src.features.led import enableLED, disableLED  # Import LED functions
from src.features.move import move, stop  # Import motor functions
from src.features.infra_shot_test import send_shot

# Configuration du socket UDP
PORT = 5005
BUFFER_SIZE = 1024

# Assurez-vous que l'IP du Raspberry Pi correspond à celle utilisée dans le premier script
RASPBERRY_IP = "192.168.0.133"

# Initialisation du socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((RASPBERRY_IP, PORT))

led_on = False  # État des LEDs
movement = None  # Stocke le mouvement en cours

# Mappage des boutons de la manette vers les actions
BUTTON_MAP = {
    3: "forward",   # Exemple : bouton A (selon la manette)
    0: "backward",  # Exemple : bouton B
    2: "left",      # Exemple : bouton X
    1: "right",     # Exemple : bouton Y
    4: "led",       # Exemple : bouton L1 pour LED
    9: "shoot"      # Exemple : bouton R1 pour tir
}

try:
    print("Attente des commandes de la manette...")
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode().strip()
        print(message)
        if message == "99":
            if movement:
                print("stop")
                stop()
                movement = None
            continue
        
        buttons_pressed = list(map(int, message.split(",")))
        
        for button in buttons_pressed:
            action = BUTTON_MAP.get(button)
            if action == "forward" and movement != "forward":
                move("forward")
                movement = "forward"
            elif action == "backward" and movement != "backward":
                move("backward")
                movement = "backward"
            elif action == "left" and movement != "left":
                move("left")
                movement = "left"
            elif action == "right" and movement != "right":
                move("right")
                movement = "right"
            elif action == "led":
                led_on = not led_on
                if led_on:
                    enableLED(Color(0, 255, 0))
                else:
                    disableLED()
            elif action == "shoot":
                send_shot()
        
        time.sleep(0.05)  # Réduction de la charge CPU

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    stop()
    disableLED()
    GPIO.cleanup()
    sock.close()
