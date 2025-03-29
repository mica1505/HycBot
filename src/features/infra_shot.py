import uuid
from src.features import InfraLib
from rpi_ws281x import Color

class ShotController:
 
    def send_shot(self):
        InfraLib.IRBlast(uuid.getnode(), "LASER")
