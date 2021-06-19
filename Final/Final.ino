#include <Servo.h>

int x;
int pos = 90;
float final = 0;
Servo myservo;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(8, OUTPUT);
  myservo.attach(9);
  myservo.write(pos);
}

void loop() {
  while (!Serial.available());
  x = Serial.readString().toInt();  
  Serial.println(x);
  if (x == 1){
      pos = pos - x;
      myservo.write(pos);
    }
  else if (x == 2){
      pos = pos + x;
      myservo.write(pos);
    }
}
