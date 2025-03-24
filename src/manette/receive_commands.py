import socket
from src.features.move import move, stop  # Import motor functions
from src.features.infra_shot_test import send_shot
import time
# Parametres reseau
PORT = 5005
BUFFER_SIZE = 1024

# Initialisation du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print(f"Serveur en attente sur le port {PORT}...")
movement = None
while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode()
    print("1",message)
   
    if message == "None":
        print("Aucun bouton press")
    #     continue

    boutons = list(map(int, message.split(",")))
    print(f"Boutons presss : {boutons}")
    if boutons:
        # Exemple d?actions
        if 0 ==boutons[-1]:  # Supposons que le bouton 0 allume un moteur
            move("backward")
            movement="backward"
        elif 1 ==boutons[-1]:  # Supposons que le bouton 1 recule
            move("right")
            movement="right"
        elif 2 ==boutons[-1]:  # Supposons que le bouton 2 tourne  gauche
            move("left")
            movement="left"
        elif 3 ==boutons[-1]:  # Supposons que le bouton 3 tourne  droite
            move("forward")
            movement="forward"
        elif 9 ==boutons[-1]:  # Supposons que le bouton 9 arrte tout
            send_shot()
        elif 10 ==boutons[-1]:
            send_shot()

        time.sleep(1)
        if movement:
            stop()
            movement= None

    # TODO : Ajouter la gestion des moteurs ici
    # Exemple : si bouton[0] == 1 ? arreter les moteurs


"""
        # Exemple d?actions
        if 0 or 12 ==boutons[-1]:  # Supposons que le bouton 0 allume un moteur
            print("? down")
        if 1 or 14 ==boutons[-1]:  # Supposons que le bouton 1 recule
            print("? droite")
        if 2 or 13 ==boutons[-1]:  # Supposons que le bouton 2 tourne  gauche
            print("? Tourner gauche")
        if 3 or 11 ==boutons[-1]:  # Supposons que le bouton 3 tourne  droite
            print("? UP")
        if 9 ==boutons[-1]:  # Supposons que le bouton 9 arrte tout
            print("? Arrt d'urgence !") 
"""

