#define intensity = 13; //intensity controlled led
#define ldrPin = A0;// intensity check factor LDR
#define trigPin 6 // for ultrasonic sensor
#define echoPin 7
#define motion 12 //distance triggered LED
#define check = A1;//Fault detector LDR 
void setup() {

Serial.begin(9600);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
pinMode(intensity, OUTPUT);
pinMode(motion, OUTPUT);
pinMode(ldrPin, INPUT);
pinMode(check, INPUT);
}

void loop() {
long duration, distance;
//triggering ultrasonic sensor
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;

int ldrStatus = analogRead(ldrPin);
int checkstatus=analogRead(check);
//LDR triggered LED
if (ldrStatus >= 60) {

digitalWrite(intensity, LOW);

} else {

digitalWrite(intensity, HIGH);
//if light should be on and the LDR near the light shows low, then light is faulty and it sends a message to take action
if( checkstatus < 20){
  Serial.print("Faulty bulb detected. Please contact authorities\n");
  
}
}


//if using PIR motion sensor instead of HC-SR04

/*if(digitalRead(7) == HIGH) // reading the data from the pir sensor
{
 //digitalWrite(13, HIGH); // setting led to high
 digitalWrite(12, HIGH); // setting buzzer to high
 Serial.println("motion detected");
 
}
else {
 //digitalWrite(13, LOW); // setting led to low
 digitalWrite(12, LOW); // setting buzzer to low
 Serial.println("scanning");
}*/

//distance triggering
if (distance < 50) {  
    digitalWrite(motion,HIGH);
}
  else {
    digitalWrite(motion,LOW);
 
  }
  if (distance >= 200 || distance <= 0){
    digitalWrite(motion,LOW);
  }
  delay(500);
}
