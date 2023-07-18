import paho.mqtt.client as mqtt
import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
import time
import socket

# Configurar broker MQTT
broker_address = socket.gethostbyname(socket.gethostname())
topic = "Sincro" #Tópico donde se publica el epoch de sincronismo
subscribe_topic = "Data/Sensor1" #Tópico al que se suscribe
subscribe_topic = "Data/Sensor2" #Tópico al que se suscribe
subscribe_topic = "Data/Sensor3" #Tópico al que se suscribe

# Archivo Logger CSV
csv_filename = "data.csv"
csv_fieldnames = ["timestamp", "payload"]

# PyQt GUI setup
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

message_textedit = None

current_epoch = int(time.time())

# Button and text display setup
button_layout = QHBoxLayout()
button = QPushButton("Enviar Sincronismo")
button_layout_2 = QHBoxLayout()
button_2 = QPushButton("STOP")
text_display = QTextEdit()
text_display.setReadOnly(True)
button_layout.addWidget(button)
button_layout_2.addWidget(button_2)
layout.addLayout(button_layout)
layout.addLayout(button_layout_2)
layout.addWidget(text_display)

# MQTT message handler
def on_message(client, userdata, message):
    payload_str = message.payload.decode("utf-8")
    print(f"Received message: {payload_str}")
    with open(csv_filename, "a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames)
        writer.writerow({
            "timestamp": message.timestamp,
            "payload": payload_str
        })
    text_display.append(f"{payload_str}\n")
    #text_display.setText(f"{payload_str}\n")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(subscribe_topic)

# Button click handler
def on_button_click():
    client.publish(topic, int(time.time()))

# Función para enviar un 0 y frenar la publicación
def on_button_click_2():
    client.publish(topic, 0)

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(broker_address)
client.subscribe(topic)

# Start the MQTT client loop
client.loop_start()

# Set button click handler
button.clicked.connect(on_button_click)
button_2.clicked.connect(on_button_click_2)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
