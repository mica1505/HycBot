import RPi.GPIO as GPIO
import time

# Définition des broches GPIO des capteurs
SENSOR_LEFT = 38   # Capteur gauche
SENSOR_MIDDLE = 36 # Capteur milieu
SENSOR_RIGHT = 35  # Capteur droit

# Initialisation des GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_LEFT, GPIO.IN)
GPIO.setup(SENSOR_MIDDLE, GPIO.IN)
GPIO.setup(SENSOR_RIGHT, GPIO.IN)

def read_sensors():
    """Read the state of the three sencors

        Returns:
        Dict[String : Bool] : True if it white False if black
    """

    left = "blanc" if GPIO.input(SENSOR_LEFT) == 0 else "noir"
    middle = "blanc" if GPIO.input(SENSOR_MIDDLE) == 0 else "noir"
    right = "blanc" if GPIO.input(SENSOR_RIGHT) == 0 else "noir"
    
    return {"Gauche" : left, "Milieu" : middle, "Droite" : right}

def detect_transition_zone():
    """Check the three capteurs if they detect white ground.

        Returns:
            Dict[String : String] : True if it white False if black

    """

    try:
        previous_states = read_sensors()  # État initial des capteurs
        print(previous_states)

        start_time = time.time()  # Enregistre le temps de départ
        
        while time.time() - start_time < 10:  # Boucle active pendant 10 secondes
            current_states = read_sensors()  # Lecture des nouveaux états

            # Vérifier si un des capteurs a changé d'état
            for sencor in current_states.keys():
                if current_states[sencor] != previous_states[sencor]:
                    print(f"🔄 Transition détectée sur {sencor}: {previous_states[sencor]} -> {current_states[sencor]}")

            previous_states = current_states  # Mise à jour de l'état précédent
            time.sleep(0.5)  # Vérification toutes les 100ms

        print("⏳ Fin de la détection après 10 secondes.")

    finally:
        GPIO.cleanup()  # Nettoyage des GPIO

# Lancer la détection des transitions
detect_transition_zone()
