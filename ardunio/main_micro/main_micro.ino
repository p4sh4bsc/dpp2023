

int pot_1, pot_2, pot_3;

int joy1x, joy1y;

bool btn_1;
bool btn_2;
bool btn_3;


String str;

void setup() {
  Serial.begin(9600);

  pinMode(A0, INPUT);   //btn_1
  pinMode(8, INPUT);   //btn_2
  pinMode(7, INPUT);   //btn_3 центр

  pinMode(A7, INPUT);  //pot_1
  pinMode(A11, INPUT); //pot_2
  pinMode(A2, INPUT); //pot_3

  pinMode(A10, INPUT); //joy_1_x
  pinMode(A9, INPUT);  //joy_1_y

  pinMode(A5, OUTPUT);  //led


}

void loop() {

  if (Serial.read() == 'H') {
    digitalWrite(A5, HIGH);
  }
  else if (Serial.read() == 'L') {
    digitalWrite(A5, LOW);
  }


  pot_1 = analogRead(A7);
  pot_2 = analogRead(A11);
  pot_3 = analogRead(A2);

  joy1x = analogRead(A10);
  joy1y = analogRead(A9);



  btn_1 = digitalRead(A0);
  btn_2 = digitalRead(8);
  btn_3 = digitalRead(7);  

  // крч, если х==1023 => Вперед;
  //           x==0 => назад;
  //           y==0 => right;
  //           y==1023 => left;
  str = String(pot_1) + " " + String(pot_2) + " " + String(pot_3) + " " + String(joy1x) + " " + String(joy1y) + " " + String(btn_1) + " " + String(btn_2) + " " + String(btn_3);
  Serial.println(str);
  delay(500);




}
