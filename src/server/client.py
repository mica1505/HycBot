import paho.mqtt.client as mqtt
import time
import uuid

# MQTT Broker settings
BROKER = "192.168.0.125"  # Make sure this is the correct IP of the broker
PORT = 1883  # Default MQTT port
TOPIC = "init"

# This will store the client ID, which we can modify to simulate a unique participant
client_id = str(uuid.getnode())

print(client_id)

# The callback function when a message is received
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode('utf-8')} on topic: {message.topic}")

# Setup the MQTT client
client = mqtt.Client(str(client_id))
client.on_message = on_message  # Set the callback for received messages

# Connect to the MQTT broker
client.connect(BROKER, PORT)

# Subscribe to the topic to listen for messages (in case the server sends any feedback)
client.subscribe("tanks/+/init")

# Start the MQTT client loop to listen for messages
client.loop_start()

# Wait for a second to ensure we're connected
time.sleep(1)

# Send the INIT message to trigger the server to assign this client to a team
init_message = f"INIT {client_id}"  # This could be any unique identifier for the player
client.publish(TOPIC, init_message)
print(f"Sent INIT message: {init_message}")

# Publier le message lorsque le robot entre dans la zone de capture
def notify_flag_zone(arg):
    topic = f"tanks/{client_id}/flag"
    message = arg
    client.publish(topic, message)
    print(f"Message envoyé : {message} sur le topic {topic}")

# Publier le message lorsque le robot entre dans la zone de capture
def shoot(arg):
    topic = f"tanks/{client_id}/shots"
    message = "SHOT_BY " + str(arg)
    print(message)
    client.publish(topic, message)
    print(f"Message envoyé : {message} sur le topic {topic}")

# Wait a bit to ensure the message is processed
time.sleep(2)

# Stop the MQTT client loop after we are done
client.loop_stop()
