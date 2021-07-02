#include <util/atomic.h> // For the ATOMIC_BLOCK macro
#include <Wire.h>

const byte scl = A5;
const byte sda = A4;
int addrResistor;
byte SLAVE_ADDR;

byte ENCA = 2;
byte ENCB = 3;
byte PWM = 5;
byte IN2 = 6;
byte IN1 = 7;

volatile long posi = 0; // specify posi as volatile: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
long prevT = 0;
float eprev = 0;
float eintegral = 0;

long target;

// PID constants
float kp = 0.046;
float kd = 0.1;
float ki = 0;

void setup() {
  Serial.begin(9600);

  addrResistor = analogRead(A0);
  if (addrResistor > 978 -5 and addrResistor < 978+5){
    addrResistor = 470;
    SLAVE_ADDR = 9;
    ENCA = 3;
    ENCB = 2;
    PWM = 5;
    IN2 = 6;
    IN1 = 7;
  }
  if (addrResistor > 958 -5 and addrResistor < 958+5){
    addrResistor = 680;
    SLAVE_ADDR = 10;
    ENCA = 2;
    ENCB = 3;
    PWM = 5;
    IN2 = 6;
    IN1 = 7;
  }
  if (addrResistor > 511 -5 and addrResistor < 511+5){
    addrResistor = 10000;
    SLAVE_ADDR = 11;
    ENCA = 2;
    ENCB = 3;
    PWM = 5;
    IN2 = 7;
    IN1 = 6;  }
  if (addrResistor > 839 -5 and addrResistor < 839+5){
    addrResistor = 2200;
    SLAVE_ADDR = 12;
    ENCA = 3;
    ENCB = 2;
    PWM = 5;
    IN2 = 6;
    IN1 = 7;
  }

  pinMode(ENCA,INPUT_PULLUP);
  pinMode(ENCB,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoderA,RISING);
//  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoderA,FALLING);
  attachInterrupt(digitalPinToInterrupt(ENCB),readEncoderB,RISING);
//  attachInterrupt(digitalPinToInterrupt(ENCB),readEncoderB,FALLING);

  Wire.begin(SLAVE_ADDR); // join I2C
  Wire.onRequest(requestEvent); 
  Wire.onReceive(receiveEvent);
  
  pinMode(PWM,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  
  Serial.println("target pos");
}

void loop() {

  // set target position
  //target = 10;
  //target = 250*sin(prevT/1e6);



  // time difference
  long currT = micros();
  float deltaT = ((float) (currT - prevT))/( 1.0e6 );
  prevT = currT;

  // Read the position in an atomic block to avoid a potential
  // misread if the interrupt coincides with this code running
  // see: https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
  long pos = 0; 
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    pos = posi;
  }
  
  // error
  long e = pos - target;

  // derivative
  float dedt = (e-eprev)/(deltaT);

  // integral
  float eintegralZwischenwert = eintegral + e*deltaT;

  // control signal
  float u = kp*e + kd*dedt + ki*eintegralZwischenwert;

  // motor power
  int pwr = (int) fabs(u);
  if( pwr > 255 ){
    pwr = 255;
//    eintegral = eintegralZwischenwert;
  }
  else{
    eintegral = eintegralZwischenwert;
  }

  // motor direction
  int dir = 1;
  if(u<0){
    dir = -1;
  }

  // signal the motor
  setMotor(dir,pwr,PWM,IN1,IN2);


  // store previous error
  eprev = e;
//  Serial.print("Kp: ");
//  Serial.print(kp);
//  Serial.print("\t");
//  Serial.print("Ki: ");
//  Serial.print(ki);
//  Serial.print("\t");
//  Serial.print("Kd: ");
//  Serial.print(kd);
//  Serial.print("\t");
  Serial.print(target);
  Serial.print("\t");
  Serial.print(pos);
  Serial.println();
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2){
  analogWrite(pwm,pwmVal);
  if(dir == 1){
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
  }
  else if(dir == -1){
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
  }
  else{
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
  }  
}

void readEncoderA(){
  int b = digitalRead(ENCB);
  if(b > 0){
    posi++;
  }
  else{
    posi--;
  }
}
void readEncoderB(){
  int b = digitalRead(ENCA);
  if(b > 0){
    posi--;
  }
  else{
    posi++;
  }
}

void sendLong(long value){
  for(int k=0; k<4; k++){
    byte out = (value >> 8*(3-k)) & 0xFF;
    Wire.write(out);
  }
}

long receiveLong(){
  long outValue;
  for(int k=0; k<4; k++){
    byte nextByte = Wire.read();
    outValue = (outValue << 8) | nextByte;
  }
  return outValue;
}

float receiveFloat(){
  int zwischenwert;
  for(int k=0; k<2; k++){
    byte nextByte = Wire.read();
    zwischenwert = (zwischenwert << 8) | nextByte;
  }
  float outValue = float(zwischenwert) / 100.0;
  return outValue;
}

void requestEvent(){
  sendLong(posi);
}

void receiveEvent(int howMany){
  kp = receiveFloat();
  ki = receiveFloat();
  kd = receiveFloat();
  target = receiveLong();
  eprev = 0;
  eintegral = 0;
  prevT = micros();
}
