import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Aucune manette détectée !")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Manette détectée : {joystick.get_name()}")

while True:
    pygame.event.pump()
    axe_gauche_x = joystick.get_axis(0)  # Joystick gauche (X)
    axe_gauche_y = joystick.get_axis(1)  # Joystick gauche (Y)
    bouton_croix = joystick.get_button(0)  # Bouton Croix

    print(f"Joystick X: {axe_gauche_x:.2f}, Y: {axe_gauche_y:.2f}, Croix: {bouton_croix}")

