const int intensity = 13;
//const int motion= 12;
const int ldrPin = A0;
//int PIR_output=7; 
#define trigPin 6
#define echoPin 7
#define motion 12
const int check = A1;
void setup() {

Serial.begin(9600);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
pinMode(intensity, OUTPUT);
pinMode(motion, OUTPUT);
pinMode(ldrPin, INPUT);
pinMode(check, INPUT);
//pinMode(PIR_output, INPUT);
}

void loop() {
long duration, distance;
digitalWrite(trigPin, LOW);  // Added this line
delayMicroseconds(2); // Added this line
digitalWrite(trigPin, HIGH);
delayMicroseconds(10); // Added this line
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;

int ldrStatus = analogRead(ldrPin);
int checkstatus=analogRead(check);

if (ldrStatus >= 60) {

digitalWrite(intensity, LOW);
Serial.print("BRIGHT\n");

//Serial.println(ldrStatus);

} else {

digitalWrite(intensity, HIGH);

Serial.print("DARK\n");

//Serial.println(ldrStatus);

if( checkstatus < 20){
  Serial.print("Faulty bulb detected. Please contact authorities\n");
  //Serial.print(checkstatus);
  
}
else 
{
  //Serial.print("Working fine\n");
  //Serial.print(checkstatus);
}
}
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
if (distance < 50) {  // This is where the LED On/Off happens
    digitalWrite(motion,HIGH); // When the Red condition is met, the Green LED should turn off
}
  else {
    digitalWrite(motion,LOW);
 
  }
  if (distance >= 200 || distance <= 0){
    //Serial.println("Out of range");
    digitalWrite(motion,LOW);
  }
  else {
    //Serial.print(distance);
    //Serial.println(" cm");
  }
  delay(500);
}
