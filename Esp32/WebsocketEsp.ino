#include <WiFi.h>
#include <WebSocketsServer.h>
#include <stdio.h>

// Constants
const char* ssid = "NOMEWIFI";
const char* password = "SENHA";

int count = 0;
String isClicked ="No";
int val;
String valorCorreto;
uint8_t ipx;

int transmit = 0;
// Globals
WebSocketsServer webSocket = WebSocketsServer(80);

// Called when receiving any WebSocket message
void onWebSocketEvent(uint8_t num,
                      WStype_t type,
                      uint8_t * payload,
                      size_t length) {

  // Figure out the type of WebSocket event
  switch(type) {

    // Client has disconnected
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;

    // New client has connected
    case WStype_CONNECTED:
      {
        ipx = num;
        IPAddress ip = webSocket.remoteIP(num);
        Serial.printf("[%u] Connection from ", num);
        Serial.println(ip.toString());
      }
      break;

    // Recebeu texto
    case WStype_TEXT:
      Serial.printf("[%u] Text: %s\n", num, payload);
      //String Site = (char*)payload;
      //webSocket.sendTXT(num, isClicked);
      char valor[30];
      memset(valor, 0, sizeof(valor));
      snprintf(valor, sizeof(valor)-1, "%d", val);
      webSocket.sendTXT(num, valor);
      valorCorreto = valor;
      Serial.println("Enviado" + valorCorreto);
      break;

    // For everything else: do nothing
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

void setup() {
  val = 0;
  // Start Serial port
  Serial.begin(9600);

  // Connect to access point
  Serial.println("Connecting");
  WiFi.begin(ssid, password);
  while ( WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }

  // Print our IP address
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server and assign callback
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {
  val = analogRead(36);
  count++;
  // Look for and handle WebSocket data
  webSocket.loop();
  if(count == 10000){
    /*
     int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);
  // print out the value you read:
    Serial.println(voltage);*/
    if(val > 1000){//isClicked == "Não"
      isClicked = "SIM";
      }else{
        isClicked = "Não";
     }
     count = 0;
       Serial.println("Botão ligado?" + isClicked);
       Serial.println(val);
       /*char valor[30];
      memset(valor, 0, sizeof(valor));
      snprintf(valor, sizeof(valor)-1, "%d", val);
      webSocket.sendTXT(ipx, valor);//Sobrecarregando valores
      valorCorreto = valor;
      Serial.println("Enviado" + valorCorreto);*/
  }
}
