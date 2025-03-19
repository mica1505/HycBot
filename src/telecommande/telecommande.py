

import RPi.GPIO as GPIO
import curses
import time
from rpi_ws281x import Color

from src.features.led import enableLED, disableLED  # Import LED functions
from src.features.move import move, stop  # Import motor functions
from src.features.infra_shot_test import send_shot


def control_robot(stdscr):
    led_on = False  # Track LED state
    stdscr.nodelay(True)  # Mode non-bloquant
    stdscr.clear()
    stdscr.addstr("Use arrow keys to move. Press 'L' to toggle LEDs. Press 'Q' to quit.\n")

    movement = None  # Stocke le mouvement en cours

    try:
        while True:
            key = stdscr.getch()

            # Détection du mouvement
            if key == curses.KEY_UP:
                if movement != "forward":
                    #stdscr.addstr("Moving Forward\n")
                    move("forward")
                    movement = "forward"
            elif key == curses.KEY_DOWN:
                if movement != "backward":
                    #stdscr.addstr("Moving Backward\n")
                    move("backward")
                    movement = "backward"
            elif key == curses.KEY_LEFT:
                if movement != "left":
                    #stdscr.addstr("Turning Left\n")
                    move("left")
                    movement = "left"
            elif key == curses.KEY_RIGHT:
                if movement != "right":
                    #stdscr.addstr("Turning Right\n")
                    move("right")
                    movement = "right"
            elif key in [ord('l'), ord('L')]:  # Gestion LED
                led_on = not led_on
                if led_on:
                    stdscr.addstr("LEDs On\n")
                    enableLED(Color(0, 255, 0))
                else:
                    stdscr.addstr("LEDs Off\n")
                    disableLED()
                #time.sleep(0.2)  # Évite les basculements trop rapides
            elif key in [ord('q'), ord('Q')]:  # Quitter
                stdscr.addstr("Exiting...\n")
                stop()
                disableLED()
                break
            elif key in [ord('s'), ord('Q')]:
                stdscr.addstr("Shoting...\n")
                send_shot()
            else:
                # Si aucune touche directionnelle n'est pressée, arrêter le mouvement
                if movement:
                    stop()
                    movement = None

            time.sleep(0.05)  # Boucle plus rapide pour meilleure réactivité

    except KeyboardInterrupt:
        stdscr.addstr("\nKeyboard interrupt detected.\n")

    finally:
        stdscr.addstr("Cleaning up GPIO...\n")
        stop()
        disableLED()
        GPIO.cleanup()

if __name__ == "__main__":
    curses.wrapper(control_robot)
