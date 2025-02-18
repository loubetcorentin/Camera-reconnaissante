//----------------------------------
//            LIBS
#include <PubSubClient.h>
#include <WiFi.h>
#include <ESP32Servo.h> // Bibliothèque pour gérer les servomoteurs

//----------------------------------
//        MQTT CONTROLLER
const char* ssid = "Mi 9 Lite";
const char* password = "corentin01";
const char* mqttServer = "192.168.43.83";
const int mqttPort = 1883;

int Val1, Val2, Val3, Val4; // Valeurs pour les quatres moteurs

#define PIN_SG90_1 10 // Broche de sortie pour le moteur 1
#define PIN_SG90_2 9  // Broche de sortie pour le moteur 2
#define PIN_SG90_3 8 // Broche de sortie pour le moteur 3
#define PIN_SG90_4 7  // Broche de sortie pour le moteur 4

Servo servo1; // Objet Servo pour le moteur 1
Servo servo2; // Objet Servo pour le moteur 2
Servo servo3; // Objet Servo pour le moteur 3
Servo servo4; // Objet Servo pour le moteur 4

WiFiClient espClient;
PubSubClient client(espClient);

//----------------------------------
//     WIFI CONNECT / RECONNECT
void setup_wifi() {
  delay(10);
  // Connexion au réseau WiFi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Boucle de reconnexion au MQTT
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("espc3-motors")) {
      Serial.println("connected");
      // S'abonner aux sujets
      client.subscribe("motor1"); // Sujet pour le moteur 1
      client.subscribe("motor2"); // Sujet pour le moteur 2
      client.subscribe("motor3"); // Sujet pour le moteur 3
      client.subscribe("motor4"); // Sujet pour le moteur 4
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

//----------------------------------
//            CALLBACK
void callback(char* topic, byte* payload, unsigned int length) {
  String top = topic;
  String msg;
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  int val = msg.toInt();
  Serial.print("Message arrived in topic: ");
  Serial.print(top);
  Serial.print(" \t Message: ");
  Serial.println(val);

  // Action en fonction du sujet reçu
  if (String(topic) == "motor1") {
    servo1.write(val); // Commande le moteur 1
    Val1 = val;        // Mémoriser la valeur reçue pour le moteur 1
  } else if (String(topic) == "motor2") {
    servo2.write(val); // Commande le moteur 2
    Val2 = val;        // Mémoriser la valeur reçue pour le moteur 2
  } else if (String(topic) == "motor3") {
    servo3.write(val); // Commande le moteur 3
    Val3 = val;        // Mémoriser la valeur reçue pour le moteur 3
  } else if (String(topic) == "motor4") {
    servo4.write(val); // Commande le moteur 4
    Val4 = val;        // Mémoriser la valeur reçue pour le moteur 4
  }
}

void setup() {
  Serial.begin(115200);

  setup_wifi();

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  // Initialisation des moteurs
  servo1.attach(PIN_SG90_1); // Attacher le moteur 1 à la broche 10
  servo2.attach(PIN_SG90_2); // Attacher le moteur 2 à la broche 9
  servo3.attach(PIN_SG90_3); // Attacher le moteur 3 à la broche 8
  servo4.attach(PIN_SG90_4); // Attacher le moteur 4 à la broche 7

  servo1.write(90); // Position initiale du moteur 1 à 90° (neutre)
  servo2.write(90); // Position initiale du moteur 2 à 90° (neutre)
  servo3.write(90); // Position initiale du moteur 3 à 90° (neutre)
  servo4.write(90); // Position initiale du moteur 4 à 90° (neutre)
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
