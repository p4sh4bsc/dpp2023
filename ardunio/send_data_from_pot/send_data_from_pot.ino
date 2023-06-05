const int buttonPin = 2;

 
void setup() {
  
  pinMode(buttonPin, INPUT);
  pinMode(A1, INPUT);
}
 
void loop(){
  
  int rotat;

 

  rotat = analogRead(A1);


  if (buttonState == HIGH) {   
    Serial.println(1);
  }
  else {

  Serial.println(0);
  }
  delay(1000);
  Serial.println(rotat);
  delay(100);
}
