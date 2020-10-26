import paho.mqtt.client as mqtt
import threading

DOMAIN = 'galiold.ir'   
PORT = 1883
KEEPALIVE = 60

trolley_positions = {}

class MQTTClient(mqtt.Client):
    global trolley_positions

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe('GPS')

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        try:
            res = list(map(lambda x: x.replace('\x00', ''), msg.payload.decode().split()))
            trolley_positions[int(res[0])] = [float(res[1]), float(res[2])]
            print(trolley_positions)
        except:
            print('Invalid input recieved: {}'.format(msg.payload.decode()))

    def start(self):
        self.connect(DOMAIN, PORT, KEEPALIVE)

