import sys
import paho.mqtt.client as mqtt
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5.QtCore import QTimer
import socket

from interfaz import Ui_MainWindow

class Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.i = 0 
        #self.voltageMin = 180 
        #self.voltageMax = 180
        #self.ui.lcdNumberCur.display(self.i)

        self.ui.pushButton.clicked.connect(self.sendSincro) #Asociar la funcion enviar epoch para sincronizar
        # self.ui.pushButton.clicked.connect(self.on_message) #Asociar la funcion enviar epoch para sincronizar
        self.ui.ei.text()
        self.ui.pushButton_stop.clicked.connect(self.sendStop) #Asociar la funcion enviar cero para frenar
        
        self.ui.lcdPresion1.display(128)
        self.ui.lcdTemperatura1.display(64)
        self.ui.lcdPresion2.display(256)
        self.ui.lcdTemperatura2.display(32)
        self.show()
        
        # Configurar broker MQTT
        self.broker_address = socket.gethostbyname(socket.gethostname()) #Obtener el IP de la maquina = IP del broker
        self.topic = "Sincro" #Tópico donde se publica el epoch de sincronismo
        self.subscribe_topic_1 = "Sensor" #Tópico al que se suscribe con información del nodo 1
        self.subscribe_topic_2 = "Sensor2" #Tópico al que se suscribe con información del nodo 1
        # MQTT client setup
        self.client = mqtt.Client()
        self.client.on_message = self.on_message #Ejecución de la funcion "on_message" cuando hay una lectura
        self.client.on_connect = self.on_connect #Conexión al Ejecución de la funcion "on_message" cuando hay una lectura
        self.client.connect(self.broker_address) #Conexión al Broker
        self.client.subscribe(self.subscribe_topic_1) #Suscripción al tópico Sensor
        self.client.subscribe(self.subscribe_topic_2) #Suscripción al tópico Sensor2
        self.client.loop_start()
        # Archivo Logger CSV
        self.csv_filename = "data.csv"
        self.csv_fieldnames = ["Calibracion","Presion","Temperatura","Sensor"]
        
    # MQTT message handler y actualizador del Loggers
    def on_message(self, client, userdata, message):
        #self.ui.lcdNumberMax.display(12)
        payload_str = message.payload.decode("utf-8")
        payload_str = payload_str.split(' | ') #Separa el string que viene con el caracter |
        topic_str = message.topic
        type(topic_str)
        if(message.topic == self.subscribe_topic_1):
            self.ui.lcdPresion1.display(payload_str[0])
            self.ui.lcdTemperatura1.display(payload_str[2])
        elif(message.topic == self.subscribe_topic_2):
            self.ui.lcdPresion2.display(payload_str[0])
            self.ui.lcdTemperatura2.display(payload_str[2])
        with open(self.csv_filename, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.csv_fieldnames)
            writer.writerow({
                "Calibracion": payload_str[1],
                "Presion": payload_str[0],
                "Temperatura": payload_str[2],
                "Sensor": message.topic
            })

    # Conexión al broker MQTT
    def on_connect(self,client, userdata, flags, rc):
        print("Conectado al broker MQTT con código " + str(rc))
        self.client.subscribe(self.subscribe_topic_1)
        self.client.subscribe(self.subscribe_topic_2)

    #Funcion para enviar cero para frenar
    def sendStop(self):
        self.client.publish(self.topic, 0)
    
    #Funcion para enviar epoch para sincronizar
    def sendSincro(self):
        self.ui.ei.text()
        self.client.publish(self.topic, self.ui.ei.text())
        #self.client.publish(self.topic, int(time.time()))

    def startTimer(self):    
        if self.ui.pushButton.text() == "Start Timer":
            self.timer.start(1000) 
            self.ui.pushButton.setText("Stop Timer")            
        else:
            self.ui.pushButton.setText("Start Timer")
            self.timer.stop() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = Form()
    sys.exit(app.exec_())