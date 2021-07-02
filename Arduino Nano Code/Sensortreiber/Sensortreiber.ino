//const byte echos[6] = {Echo1, Echo2, Echo3, Echo4, Echo5, Echo6};
//const byte trigs[6] = {Trig1, Trig2, Trig3, Trig4, Trig5, Trig6};



// IC2 Bus
#include <Wire.h>
const byte scl = A5;
const byte sda = A4;
#define SLAVE_ADDR 8
// Define counter to count bytes in response
byte bcount = 0;

//const byte Echo3 = 32;
//const byte Trig3 = 33;
//const byte Echo4 = 34;
//const byte Trig4 = 35;
//const byte Echo1 = 36;
//const byte Trig1 = 37;
//const byte Echo2 = 38;
//const byte Trig2 = 39;
//const byte Echo5 = 40;
//const byte Trig5 = 41;
//const byte Echo6 = 42;
//const byte Trig6 = 43;
//const byte echos[6] = {Echo1, Echo2, Echo3, Echo4, Echo5, Echo6};
//const byte trigs[6] = {Trig1, Trig2, Trig3, Trig4, Trig5, Trig6};


const byte echos[] = {3, 5, 7, 9, 11, 13};
const byte trigs[] = {2, 4, 6, 8, 10, 12};

const int amountOfSensors = sizeof(trigs)/sizeof(trigs[0]);
long distances[amountOfSensors];


const int SENSOR_MAX_RANGE = 254; // in cm

long lastMillis = 0L; // SystemMillis zur Zeit der letzten Entfernungsberechnung
byte pingCounter = 0L;


byte battVal = 70; //in %

// initialise ultrasonic sensors
void ultrasonicSensorsInitialising(){
//  Serial.println("Initialise ultrasonic sensors");
  for (int n=0; n<=amountOfSensors-1 ; n=n+1){
    pinMode(trigs[n], OUTPUT);
//    Serial.println(String(trigs[n]) +"Trig");
    digitalWrite(trigs[n], LOW);
    pinMode(echos[n], INPUT);
//    Serial.println(String(echos[n]) +"Echo");
    distances[n] = getDistance(n);
//    Serial.println(distances[n]);
    delay(10);
  }
//  Serial.println("First Ping");
  ping();
//  Serial.println("done");
}


// Measure the Distance in mm with sensor n
int getDistance(int n){ 
  int distance=0;
  long sensorTime=0;
  
  digitalWrite(trigs[n], LOW); 
  delayMicroseconds(1);
  noInterrupts();
  digitalWrite(trigs[n], HIGH); //Trigger impulse 10 us
 delayMicroseconds(1);
 digitalWrite(trigs[n], LOW); 
 sensorTime = pulseIn(echos[n], HIGH); // Measure the echo-time
 interrupts(); 
 distance = sensorTime * 0.03435 /2 + 1; // Convert the sensorTime into a distance    
 if (distance > SENSOR_MAX_RANGE){
  distance = SENSOR_MAX_RANGE;
 }
 return(distance);
}



// Let every sensor ping and save the distances
void ping(){
  long currentMillis = millis();
  if (pingCounter>= amountOfSensors){
    pingCounter = 0;  //Setzt den Zähler zurück, wenn er durchgelaufen ist, oder Fehler aufgetreten sind
  }
  if (currentMillis - lastMillis >= 50){   //Alle 200 Millisekunden wird eine Entfernung gemessen
//    Serial.println(pingCounter);
    distances[pingCounter] = getDistance(pingCounter);
    pingCounter++;
    lastMillis = currentMillis;
  }
}

int getVoltage(){
  // read the input on analog pin 0:
  int sensorValue = analogRead(A1);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 15000mV):
  int voltage = sensorValue * (15 *10 / 1023);
  voltage = map(sensorValue,0,1023,0,15000);
  byte value = map(voltage,12000,12900,0,100);
  // print out the value you read:
//  Serial.println(sensorValue);
//  Serial.println(voltage);
  return value;
}


void requestEvent() {
 
  // Define a byte to hold data
  byte bval;
  
  // Cycle through data
  // First response is always 255 to mark beginning
  switch (bcount) {
    case 0:
      bval = 255;
      break;
    case 1:
      bval = battVal;
      break;
    case 2:
      bval = distances[0];
      break;
    case 3:
      bval = distances[1];
      break;
    case 4:
      bval = distances[2];
      break;
    case 5:
      bval = distances[3];
      break;
    case 6:
      bval = distances[4];
      break;
    case 7:
      bval = distances[5];
      break;
  }
  
  // Send response back to Master
  Wire.write(bval);
  
  // Increment byte counter
  bcount = bcount + 1;
  if (bcount > 6) bcount = 0;
 
}






void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDR);                // join i2c bus with the defined address
  Wire.onRequest(requestEvent); // register event
  delay(20);
  // initialise ultrasonic sensors
  ultrasonicSensorsInitialising();
}

void loop() {
//  ping();
  for (byte i; i<amountOfSensors; i++){
    distances[i] = getDistance[i];
    delay(10);
  }
  battVal = getVoltage();
  delay(50);
  Serial.print("0:");
  Serial.print(distances[0]);
  Serial.print("\t");
  Serial.print("1:");
  Serial.print(distances[1]);
  Serial.print("\t");
  Serial.print("2:");
  Serial.print(distances[2]);
  Serial.print("\t");
  Serial.print("3:");
  Serial.print(distances[3]);
  Serial.print("\t");
  Serial.print("4:");
  Serial.print(distances[4]);
  Serial.print("\t");
  Serial.print("5:");
  Serial.print(distances[5]);
  Serial.println();

}
