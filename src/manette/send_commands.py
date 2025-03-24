import pygame
import socket
import time

# Adresse IP du Raspberry Pi (remplace par l'IP de ton RPi)
RASPBERRY_IP = "192.168.0.133"
PORT = 5005

# Initialisation du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialisation de pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Aucune manette détectée !")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Manette détectée : {joystick.get_name()}")

# Initialisation des variables d'état
prev_buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
last_message = None  # pour éviter de renvoyer le même message
move_sent = False

print("État initial des boutons :", prev_buttons)

try:
    while True:
        pygame.event.pump()
        
        # Lire l'état actuel des boutons
        boutons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        boutons_actifs = [i for i, val in enumerate(boutons) if val == 1]
        
        # Déterminer le message à envoyer
        if not boutons_actifs:
            message = "99"
        else:
            message = ",".join(map(str, boutons_actifs))
        
        # Envoyer le message seulement si il a changé
        if message != last_message:
            print(f"Envoi : {message}")
            try:
                sock.sendto(message.encode(), (RASPBERRY_IP, PORT))
                last_message = message
            except OSError as e:
                print(f"Erreur envoi UDP : {e}")
        
        # Petite pause pour éviter une boucle trop rapide
        time.sleep(0.05)

except KeyboardInterrupt:
    print("QUITTING")
    joystick.quit()
    pygame.quit()
