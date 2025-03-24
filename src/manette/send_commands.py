import pygame
import socket
import time
# Adresse IP du Raspberry Pi (remplace par l'IP de ton RPi)
RASPBERRY_IP = "192.168.1.176"
PORT = 5005



# Initialisation du socket UDP


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


prev_axe_x, prev_axe_y = 0, 0
# Scanner une première fois les boutons pour avoir l’état réel
pygame.event.pump()
prev_buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
move_sent = False
print("État initial des boutons :", prev_buttons)
try:
####################### BOUTONS #######################

    while True:
        pygame.event.pump()
        
        # Lire l'état actuel des boutons
        boutons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
        # boutons_actifs = [i for i, val in enumerate(boutons) if val == 1]  # Liste des boutons pressés
        boutons_actifs = [i for i, val in enumerate(boutons) if val == 1] 

        # Vérifier si un bouton a changé d'état
        if boutons_actifs and not move_sent:
            message = ",".join(map(str, boutons_actifs)) if boutons_actifs else "None"

            print(f"Envoi : {message}")  # Debug
            
            try:
                move_sent = True
                print(f"Envoi : {message}")  # Debug
                sock.sendto(message.encode(), (RASPBERRY_IP, PORT))
            except OSError as e:
                print(f"Erreur envoi UDP : {e}")

        if not any(boutons):
            move_sent=False
#             prev_buttons = boutons.copy()
###############################   JOYSTICK + BUTTONS ##################################
    # while True:
    #     pygame.event.pump()
        
    #     axe_gauche_x = round(joystick.get_axis(0), 2)  # Gauche/Droite
    #     axe_gauche_y = round(joystick.get_axis(1), 2)  # Avant/Arrière
        
    #     # Lire tous les boutons
    #     buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    #     # Vérifier si quelque chose a changé
    #     if (axe_gauche_x != prev_axe_x or axe_gauche_y != prev_axe_y or buttons != prev_buttons):
    #         # Construire un message à envoyer
    #         message = f"{axe_gauche_x},{axe_gauche_y},{','.join(map(str, buttons))}"
    #         # print(message)
    #         # print(message)

    #         try:
    #             # sock.sendto(message.encode(), (RASPBERRY_IP, PORT))
    #             print(message)
    #         except OSError as e:
    #             print(f"Erreur envoi UDP : {e}")

    #     # Mettre à jour les valeurs précédentes
    #     prev_axe_x, prev_axe_y = axe_gauche_x, axe_gauche_y
    #     prev_buttons = buttons.copy()

except KeyboardInterrupt:
    print("QUITTING")
    joystick.quit()
