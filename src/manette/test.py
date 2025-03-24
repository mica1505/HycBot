# import pygame
# import socket
# import time

# class SendCommands:
#     def __init__(self, raspberry_ip="192.168.0.133", port=5005, loop_delay=0.05):
#         self.raspberry_ip = raspberry_ip
#         self.port = port
#         self.loop_delay = loop_delay
#         self.sock = None
#         self.joystick = None
#         self.last_message = None
        
#     def initialize_socket(self):
#         """Initialise le socket UDP."""
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     def initialize_joystick(self):
#         """Initialise pygame et la manette."""
#         pygame.init()
#         pygame.joystick.init()

#         if pygame.joystick.get_count() == 0:
#             print("Aucune manette détectée !")
#             return False
        
#         self.joystick = pygame.joystick.Joystick(0)
#         self.joystick.init()
#         print(f"Manette détectée : {self.joystick.get_name()}")
#         return True

#     def get_trigger_values(self):
#         """Lit et normalise les valeurs des gâchettes L2 et R2."""
#         L2_index = 4  # Souvent l'axe 4
#         R2_index = 5  # Souvent l'axe 5

#         L2_value = self.joystick.get_axis(L2_index)
#         R2_value = self.joystick.get_axis(R2_index)

#         # Normalisation de -1 à 1 à 0 à 1
#         L2_value = (L2_value + 1) / 2
#         R2_value = (R2_value + 1) / 2

#         return L2_value, R2_value

#     def get_button_state(self):
#         """Lit l'état des boutons de la manette."""
#         num_buttons = self.joystick.get_numbuttons()
#         buttons = [self.joystick.get_button(i) for i in range(num_buttons)]
#         return buttons

#     def send_message(self, message):
#         """Envoie un message au Raspberry Pi via UDP."""
#         if message != self.last_message:
#             try:
#                 self.sock.sendto(message.encode(), (self.raspberry_ip, self.port))
#                 print(f"Envoi : {message}")
#                 self.last_message = message
#             except OSError as e:
#                 print(f"Erreur envoi UDP : {e}")

#     def main_loop(self):
#         """Boucle principale pour traiter les événements du joystick."""
#         prev_buttons = self.get_button_state()

#         try:
#             while True:
#                 # Actualiser les événements pygame
#                 pygame.event.pump()

#                 # Lire les valeurs des gâchettes
#                 L2_value, R2_value = self.get_trigger_values()

#                 # Si L2 ou R2 sont pressés, envoyer l'état des gâchettes
#                 if L2_value > 0.1 or R2_value > 0.1:
#                     trigger_message = f"L2:{L2_value:.2f}, R2:{R2_value:.2f}"
#                     print(trigger_message)
#                     self.send_message(trigger_message)

#                 # Lire l'état actuel des boutons
#                 buttons = self.get_button_state()
#                 active_buttons = [i for i, val in enumerate(buttons) if val == 1]

#                 # Créer le message à envoyer
#                 message = "99" if not active_buttons else ",".join(map(str, active_buttons))

#                 # Envoyer le message si nécessaire
#                 self.send_message(message)

#                 # Pause pour éviter une boucle trop rapide
#                 time.sleep(self.loop_delay)

#         except KeyboardInterrupt:
#             print("QUITTING")
#         finally:
#             self.clean_up()

#     def clean_up(self):
#         """Nettoyage des ressources."""
#         if self.joystick:
#             self.joystick.quit()
#         pygame.quit()
#         if self.sock:
#             self.sock.close()
#         print("Ressources libérées, programme terminé")


# if __name__ == "__main__":
#     controller = JoystickController()
    
#     # Initialiser le socket et la manette
#     if controller.initialize_joystick():
#         controller.initialize_socket()
#         controller.main_loop()


import pygame
import socket
import time

# Configuration
RASPBERRY_IP = "192.168.0.133"
PORT = 5005
LOOP_DELAY = 0.05  # Délai entre les itérations de la boucle (en secondes)

def main():
    # Initialisation du socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Initialisation de pygame et de la manette
    pygame.init()
    pygame.joystick.init()
    
    # Vérifier si une manette est connectée
    if pygame.joystick.get_count() == 0:
        print("Aucune manette détectée !")
        return
    
    # Initialiser la première manette trouvée
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Manette détectée : {joystick.get_name()}")
    
    # Initialisation des variables d'état
    last_message = None
    
    # Obtenir l'état initial des boutons
    num_buttons = joystick.get_numbuttons()
    prev_buttons = [joystick.get_button(i) for i in range(num_buttons)]
    print("État initial des boutons :", prev_buttons)
    
    try:
        while True:
            # Actualiser les événements pygame
            pygame.event.pump()
            # Indices des axes pour L2 et R2 (varie selon la manette et l'OS)
            L2_index = 4  # Souvent l'axe 4
            R2_index = 5  # Souvent l'axe 5

            # Lire l'état des gâchettes
            L2_value = joystick.get_axis(L2_index)  # De -1 à 1 (ou 0 à 1 selon le driver)
            R2_value = joystick.get_axis(R2_index)

            # Normalisation (certains drivers donnent -1 à 1, d'autres 0 à 1)
            L2_value = (L2_value + 1) / 2  # Pour obtenir une plage 0 à 1
            R2_value = (R2_value + 1) / 2

            # Seulement envoyer si L2 ou R2 sont pressés
            if L2_value > 0.1 or R2_value > 0.1:
                trigger_message = f"L2:{L2_value:.2f}, R2:{R2_value:.2f}"
                print(trigger_message)
                # sock.sendto(trigger_message.encode(), (RASPBERRY_IP, PORT))

            # Lire l'état actuel des boutons
            boutons = [joystick.get_button(i) for i in range(num_buttons)]
            boutons_actifs = [i for i, val in enumerate(boutons) if val == 1]
            
            # Créer le message à envoyer
            message = "99" if not boutons_actifs else ",".join(map(str, boutons_actifs)) #"B:"
            
            # Envoyer le message seulement s'il a changé
            if message != last_message:
                print(f"Envoi : {message}")
                try:
                    sock.sendto(message.encode(), (RASPBERRY_IP, PORT))
                    last_message = message
                except OSError as e:
                    print(f"Erreur envoi UDP : {e}")
            
            # Pause pour éviter une boucle trop rapide
            time.sleep(LOOP_DELAY)
            
    except KeyboardInterrupt:
        print("QUITTING")
    finally:
        # Nettoyage des ressources
        joystick.quit()
        pygame.quit()
        sock.close()

if __name__ == "__main__":
    main()

