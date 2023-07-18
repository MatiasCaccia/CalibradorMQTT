#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <TimeLib.h>
#include <SPI.h>
/*
Codigo para la ESP32 que se conecta al broker MQTT y espera un mensaje del tópico "Sincro"
Comienza a publicar "Lectura | Sincro" cada 200 ms al tópico "Sensor".
Se debe publicar el valor real de calibración
Enviando "0" en el tópico "Sincro" se frena la publicación
*/

/*
QUEDA CONECTAR EL OTRO BMP280 EN LA ESP32 Y VER SI FUNCIONA
*/

//-----------------------------------------------
// PINOUT
//----------------------------------------------- VCC 1 | GND 2
#define BMP_SCK  (18) //3
#define BMP_MISO (19) //6
#define BMP_MOSI (23) //4
#define BMP_CS_1 (5) //5
#define LED 2
#define BMP_CS_2 (4) //5

//-----------------------------------------------
// CONSTANTES
//-----------------------------------------------
// Broker MQTT
const char* mqtt_server = "192.168.4.2";
const int mqtt_port = 1883;
const char* mqtt_topic = "Sensor";
const char* mqtt_topic_2 = "Sensor2";
const char* sync_topic = "Sincro";
bool synced = false;  // Flag para comenzar la transmisión
float pressure1;
float temperature1;
float pressure2;
float temperature2;

// BMP280 mediante Hardware SPI
Adafruit_BMP280 bmp(BMP_CS_1); 
Adafruit_BMP280 bmp2(BMP_CS_2);

// Hotspot WiFi
const char* ap_ssid = "ESP32_HOTSPOT";
const char* ap_password = "12345678";
IPAddress ap_ip(192, 168, 4, 1);
IPAddress netmask(255, 255, 255, 0);

// Objetos de clientes WiFi y MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Variable global para la sincronización
time_t syncedTime;
float epoch;
String payloadTemp;

//-----------------------------------------------
// FUNCIONES
//-----------------------------------------------
void callback(char* topic, byte* payload, unsigned int length);

//-----------------------------------------------
// SETUP
//-----------------------------------------------
void setup() {
  pinMode(LED,OUTPUT);
  digitalWrite(LED, HIGH);  // Enciende el LED
  Serial.begin(115200);
  Serial.println("-----------------------------");
  // Generar el hotspot WiFi
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(ap_ip, ap_ip, netmask);
  WiFi.softAP(ap_ssid, ap_password);
  Serial.print("SoftAP IP address: ");
  Serial.println(WiFi.softAPIP());
  delay(5000);
  // Conectar al broker MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("MQTT connected");
    } else {
      Serial.print("MQTT failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds...");
      delay(5000);
    }
  }
  client.subscribe("Sincro");

  // BMP280
  //Serial.println(F("BMP280 test"));
  unsigned status = bmp.begin();
  unsigned status2 = bmp2.begin();
  //Configuración del datasheet
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_250); /* Standby time. */
  bmp2.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_250); /* Standby time. */
  if (!status) {
    Serial.println(F("No se envuentra el BMP1"));
    Serial.print("SensorID: 0x"); Serial.println(bmp.sensorID(),16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("        ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }
  Serial.println(F("BMP1 OK"));
  if (!status2) {
    Serial.println(F("No se envuentra el BMP2"));
    Serial.print("SensorID: 0x"); Serial.println(bmp.sensorID(),16);
    Serial.print("        ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n");
    Serial.print("        ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("        ID of 0x60 represents a BME 280.\n");
    Serial.print("        ID of 0x61 represents a BME 680.\n");
    while (1) delay(10);
  }
  Serial.println(F("BMP2 OK"));

  //Enciende el LED
  digitalWrite(LED, LOW);  
}

//-----------------------------------------------
// LOOP
//-----------------------------------------------
void loop() {
  client.loop();
  // Esperar hasta que llegue el mensaje
  if (!synced) {
    return; 
  }
  // Publicar el valor al broker MQTT
  Serial.print("Publicando al topico: ");
  Serial.println(mqtt_topic);
  Serial.print("Valor registrado: ");
  pressure1 = bmp.readPressure();
  temperature1 = bmp.readTemperature();
  Serial.println(pressure1);

  Serial.print("Publicando al topico: ");
  Serial.println(mqtt_topic_2);
  Serial.print("Valor registrado: ");
  pressure2 = bmp2.readPressure();
  temperature2 = bmp2.readTemperature();
  Serial.println(pressure2);
  
  Serial.print("| - |");
  Serial.println("---------------------");

  // Append the synchronized time to the payload
  char payload[100];
  char payload2[100];

  // Clear the contents of the resultString
  memset(payload, 0, sizeof(payload));
  memset(payload2, 0, sizeof(payload2));

  // String to concatenate
  String stringToConcat = payloadTemp;

  // Convertir el float registrado en string con dtostrf()
  char floatString[10]; // Char array to store the float as a string
  char floatStringT[10]; // Char array to store the float as a string
  char floatString2[10]; // Char array to store the float as a string
  char floatStringT2[10]; // Char array to store the float as a string
  dtostrf(pressure1, 4, 2, floatString); // Format: 4 digits, 2 decimal places
  dtostrf(temperature1, 4, 2, floatStringT); // Format: 4 digits, 2 decimal places
  dtostrf(pressure2, 4, 2, floatString2); // Format: 4 digits, 2 decimal places
  dtostrf(temperature2, 4, 2, floatStringT2); // Format: 4 digits, 2 decimal places

  // Concatenar el float, separador y string
  // Sensor 1
  strcat(payload, floatString);
  strcat(payload, " | ");
  strcat(payload,stringToConcat.c_str());
  strcat(payload, " | ");
  strcat(payload, floatStringT);
  client.publish(mqtt_topic, payload);
  
  // Sensor 2
  strcat(payload2, floatString2);
  strcat(payload2, " | ");
  strcat(payload2,stringToConcat.c_str());
  strcat(payload2, " | ");
  strcat(payload2, floatStringT2);
  client.publish(mqtt_topic_2, payload2);

  // Wait for some time before publishing again
  delay(250);
}

//-----------------------------------------------
// FUNCIONES
//-----------------------------------------------
void callback(char* topic, byte* payload, unsigned int length) {
  // Handle incoming MQTT messages here
  if (strcmp(topic, sync_topic) == 0) {
    // Synchronize time with the broker's time
    for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    payloadTemp += (char)payload[i];
    }
    epoch = atof((const char*)payload);
    synced = true;
    if(epoch == 0){
      synced = false;
      payloadTemp = "";
      Serial.println("Alto");
    }
  }  
}