#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEEddystoneURL.h>
#include <BLEEddystoneTLM.h>
#include <BLEBeacon.h>

const char *ssid = "M7GE";
const char *password = "KarimGehad2607";

const char *host = "http://192.168.2.100:8000/save-scan";

unsigned long lastTime = 0;
int intervalInSeconds = 1; // 1 second
unsigned long interval = intervalInSeconds * 1000;
int antennaId = 1;

BLEScan *pBLEScan;

char *macAddresses[] = {
    "B2:2B:0A:57:1B:2C",
    "FF:FF:30:02:3E:5C",
    "FF:FF:30:02:7C:E7",
    "FF:21:10:25:35:0C",
};

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.localIP());

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setActiveScan(true); // active scan uses more power, but get results faster
  pBLEScan->setInterval(800);
  pBLEScan->setWindow(799);
}

void loop()
{
  if (millis() - lastTime < interval)
  {
    return;
  }
  lastTime = millis();

  // we will do a bluetooth scan here
  // and then send the results to the server

  BLEScanResults foundDevices = pBLEScan->start(intervalInSeconds, false);

  for (int i = 0; i < foundDevices.getCount(); i++)
  {
    BLEAdvertisedDevice d = foundDevices.getDevice(i);
    String macAddress = d.getAddress().toString().c_str();
    macAddress.toUpperCase();

    for (int j = 0; j < sizeof(macAddresses) / sizeof(macAddresses[0]); j++)
    {
      if (macAddress.equals(macAddresses[j]))
      {
        Serial.println("Found device: " + macAddress);
        int rssi = d.getRSSI();
        Serial.println("RSSI: " + String(rssi));

        HTTPClient http;
        http.begin(host);
        http.addHeader("Content-Type", "application/json");
        String body = "{\"macAddress\": \"" + macAddress + "\", \"rssi\": " + String(rssi) + ", \"antennaId\":" + String(antennaId) + "}";
        int httpResponseCode = http.POST(body);
        if (httpResponseCode > 0)
        {
          String response = http.getString();
          Serial.println(httpResponseCode);
          Serial.println(response);
        }
        else
        {
          Serial.println("Error on sending POST: " + http.errorToString(httpResponseCode));
        }
        http.end();
      }
    }
  }
  pBLEScan->clearResults(); // delete results fromBLEScan buffer to release memory
}