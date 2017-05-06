/*
  08. April 2017
  Jan Wirwahn
  senseBox Home with SDS011 sending data over serial. Meat for processing visualization  
*/
#include <Wire.h>
#include "HDC100X.h"
#include "BMP280.h"
#include <SDS011.h>
#include <Makerblog_TSL45315.h>


//Load sensors
Makerblog_TSL45315 TSL = Makerblog_TSL45315(TSL45315_TIME_M4);
HDC100X HDC(0x43);
BMP280 BMP;
SDS011 my_sds;

//measurement variables
float pm10, pm25;
int error;
float temperature = 0;
double tempBaro, pressure;
char result;

#define UV_ADDR 0x38
#define IT_1   0x1
#define RXPIN 7
#define TXPIN 6

void setup() {
  my_sds.begin(RXPIN,TXPIN);
  Serial.begin(9600);
  sleep(1000);
  Wire.begin();
  Wire.beginTransmission(UV_ADDR);
  Wire.write((IT_1 << 2) | 0x02);
  Wire.endTransmission();
  sleep(500);
  HDC.begin(HDC100X_TEMP_HUMI, HDC100X_14BIT, HDC100X_14BIT, DISABLE);
  TSL.begin();
  BMP.begin();
  BMP.setOversampling(4);
  temperature = HDC.getTemp();
  my_sds.wakeup();
  sleep(30000); //preheating time
}

void loop() {
    result = BMP.startMeasurment();
    if (result != 0) {
      sleep(result);
      result = BMP.getTemperatureAndPressure(tempBaro, pressure);
    }else {
      tempBaro = 0;
      pressure = 0;
    }
    Serial.print(HDC.getTemp());
    Serial.print(",");
    Serial.print(HDC.getHumi());
    Serial.print(",");
    Serial.print(pressure);
    Serial.print(",");
    Serial.print(TSL.readLux());
    Serial.print(",");
    Serial.print(getUV());
    Serial.print(",");
    error = my_sds.read(&pm25,&pm10);
    if (! error) {   
      
      Serial.print(pm25);
      Serial.print(","); 
      Serial.print(pm10);
    }
    else{
      Serial.print("0");
      Serial.print(","); 
      Serial.print("0");
    }
    Serial.print("\n");
    sleep(2000);
}

uint16_t getUV() {
  byte msb = 0, lsb = 0;
  uint16_t uvValue;
  Wire.requestFrom(UV_ADDR + 1, 1); //MSB
  sleep(1);
  if (Wire.available()) msb = Wire.read();
  Wire.requestFrom(UV_ADDR + 0, 1); //LSB
  sleep(1);
  if (Wire.available()) lsb = Wire.read();
  uvValue = (msb << 8) | lsb;
  return uvValue * 5;
}

// millis() rollover fix - http://arduino.stackexchange.com/questions/12587/how-can-i-handle-the-millis-rollover
void sleep(unsigned long ms) {            // ms: duration
  unsigned long start = millis();         // start: timestamp
  for (;;) {
    unsigned long now = millis();         // now: timestamp
    unsigned long elapsed = now - start;  // elapsed: duration
    if (elapsed >= ms)                    // comparing durations: OK
      return;
  }
}
