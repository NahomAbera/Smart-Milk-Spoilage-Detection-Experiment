#include <BarometricPressure.h>

/* Creating Object of BarometricPressure Class */
BarometricPressure Pr(ULTRA_HIGH_RESOLUTION);
float altitude;

/* Setup Function */
void setup() {

  /* Setting up communication */
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(100000);
  
  /* Setting up the BarometricPressure Board. */
  for(;;)
  {
    if(Pr.begin() == true)
    {
      Serial.println("Barometric Pressure Sensor is connected");
      break;
    }
    Serial.println("Barometric Pressure Sensor is disconnected");
    delay(500u);
  }
}

/* Loop Function */
void loop() {
  
  /* Loop function continuously gets data and print at every 1 second */
  if(Pr.ping())
  {
    Pr.getTempC();
    Pr.getTempF();
    Serial.println();
  }
  delay(1000u);
}
