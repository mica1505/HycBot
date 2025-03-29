import paho.mqtt.client as mqtt
import time
import uuid

from rpi_ws281x import Color
from src.server.constantes import BROKER, PORT

class Client:
    def __init__(self):
        self.client_id = str(hex(uuid.getnode()))
        print(f"Client ID: {self.client_id}")
        
        self.client = mqtt.Client(self.client_id)
        self.client.on_message = self.on_message  # Set the callback for received messages
        
        self.connect()
        self.subscribe_topics()
        self.send_init_message()

        self.team = None
        self.qr_code = None

        self.test = None
        
    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(BROKER, PORT)
        self.client.loop_start()
        time.sleep(1)  # Ensure connection is established
    
    def subscribe_topics(self): 
        """Subscribe to necessary MQTT topics."""
        self.client.subscribe("tanks/+/init")
    
    def on_message(self, client, userdata, message):  #this function get executed whenever we receive a message
        """Callback function for received messages."""
        message_content = message.payload.decode('utf-8')
        #print(f"Received message: {message_content} on topic: {message.topic}")

        if message_content.startswith("TEAM"):
            self.team = message_content.split(" ")[1]

        elif message_content.startswith("QR_CODE"):
            self.qr_code = message_content.split(" ")[1]

        elif message_content.startswith("SCAN_FAILED"):
            self.test = "gferyvgerhjgkjrhgvkjhr"

        

    
    def send_init_message(self): 
        """Send the INIT message to be assigned to a team."""
        message = f"INIT {self.client_id}"
        self.client.publish("init", message)
        print(f"Sent INIT message: {message}")
    
    def notify_flag_zone(self, message):
         """Notify when entering the flag zone."""
         topic = f"tanks/{self.client_id}/flag"
         self.client.publish(topic, message)
         print(f"Message sent: {message} on topic {topic}")
    
    def shoot(self, shooter_id):
         """Send a shot message."""
         topic = f"tanks/{self.client_id}/shots"
         message = f"SHOT_BY {shooter_id}"
         self.client.publish(topic, message)
         print(f"Message sent: {message} on topic {topic}")
    
    def qr_win_code(self, qr):
         """Send a shot message."""
         topic = f"tanks/{self.client_id}/qr_code"
         message = f"QR_CODE {qr}"
         self.client.publish(topic, message)
         print(f"Message sent: {message} on topic {topic}")

    def get_team(self):
        """return the team of the player"""
        if self.team == "RED":
            return Color(255, 0, 0) 
        if self.team == "BLUE":
            return Color(0, 0, 255) 
        

    def get_qr_code(self):
        """init the qr code"""
        return self.qr_code

    def get_test(self):
        """init the qr code"""
        return self.test
    
    def stop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()
