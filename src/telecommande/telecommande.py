import RPi.GPIO as GPIO
import curses
import time
import threading
from rpi_ws281x import Color

from src.features.led import LEDController
from src.features.move import MotorController
from src.features.infra_shot import ShotController
from src.features.detect_color import SensorController
from src.features.stream_qr_code import Camera
from src.features.detect_shot import ShotDetector

from src.server.client import Client


import socket

from src.features.led import enableLED, disableLED  # Import LED functions
from src.features.move import move, stop  # Import motor functions
from features.infra_shot import send_shot


class Telecommande:
    def __init__(self):
        GPIO.setwarnings(False)  # Disable warnings
        GPIO.setmode(GPIO.BOARD)  # Set GPIO pin numbering mode

        self.led_controller = LEDController()
        self.motor_controller = MotorController()
        self.shot_controller = ShotController()
        self.sensor_controller = SensorController()
        self.shot_detector = ShotDetector() 
        self.camera = Camera()

        self.client = Client()
        time.sleep(5) #make sur all communication are done with the server befaure procedding  
        # self.led_controller.enable_led() #TODO : it more paractical to loop until we are asigned a team instead os just sleep 
        # self.led_controller.disable_led()

        #print("here_________",self.client.get_qr_code())
        #print("herehreh_______",self.client.get_team())

        
        # Start sensor detection in a separate thread
        self.sensor_thread = threading.Thread(target=self.sensor_controller.detect_transition_zone, daemon=True)
        self.sensor_thread.start()

        # Start shot detector in a separate thread
        self.shot_detector_thread = threading.Thread(target=self.shot_detector.detect_shot, daemon=True)
        self.shot_detector_thread.start()

        # Start camera capture in a separate thread
        self.camera_thread = threading.Thread(target=self.camera.capture_frames, daemon=True)
        self.camera_thread.start()

        # Start Flask server in a separate thread without showing output in terminal
        self.flask_thread = threading.Thread(target=self.run_flask, daemon=True)
        self.flask_thread.start()

    def run_flask(self):
        """Run the Flask app without blocking the terminal."""
        self.camera.app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)

    def control_robot(self, stdscr):
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.clear()
        stdscr.addstr("Use arrow keys to move. Press 'L' to toggle LEDs. Press 'Q' to quit.\n")
        movement = None

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
                
                time.sleep(0.05)

        except KeyboardInterrupt:
            stdscr.addstr("\nKeyboard interrupt detected.\n")
        
        finally:
            stdscr.addstr("Cleaning up GPIO...\n")
            self.motor_controller.stop()
            self.led_controller.disable_led()
            GPIO.cleanup()

if __name__ == "__main__":
    telecommande = Telecommande()
    curses.wrapper(telecommande.control_robot)

"""        
        try:

            while True:
                #print(self.client.get_test())
                id_shooter = self.shot_detector.get_shot_detected()
                if id_shooter :
                    self.client.shoot(id_shooter)
                    self.shot_detector.shot_detected =  None
                
                transition = self.sensor_controller.res
                if transition == "🔄 Transition détectée sur Gauche: noir -> blanc":
                    self.client.notify_flag_zone("ENTER_FLAG_AREA")
                    self.sensor_controller.res = None
                elif transition == "🔄 Transition détectée sur Gauche: blanc -> noir" :
                    self.client.notify_flag_zone("EXIT_FLAG_AREA")
                    self.sensor_controller.res = None

                qr = self.camera.get_qr_code()
                if qr :
                    self.client.qr_win_code(qr)
                    self.camera.qr_code = None

                key = stdscr.getch()
                # Movement controls
                if key == curses.KEY_UP:
                    if movement != "forward":
                        self.motor_controller.move("forward")
                        movement = "forward"
                elif key == curses.KEY_DOWN:
                    if movement != "backward":
                        self.motor_controller.move("backward")
                        movement = "backward"
                elif key == curses.KEY_LEFT:
                    if movement != "left":
                        self.motor_controller.move("left")
                        movement = "left"
                elif key == curses.KEY_RIGHT:
                    if movement != "right":
                        self.motor_controller.move("right")
                        movement = "right"
                elif key in [ord('l'), ord('L')]:
                    self.led_controller = LEDController()
                    self.led_controller.enable_led((0, 255, 0))
                elif key in [ord('q'), ord('Q')]:
                    print("Exiting...\n")
                    self.motor_controller.stop()
                    self.led_controller.disable_led()
                    break
                elif key in [ord('s'), ord('S')]:
                    self.shot_controller.send_shot()
                    self.led_controller = LEDController()
                    self.led_controller.enable_led(self.client.get_team()) 
                    self.led_controller.disable_led()
                else:
                    if movement:
                        self.motor_controller.stop()
                        movement = None
                
                time.sleep(0.05)
"""