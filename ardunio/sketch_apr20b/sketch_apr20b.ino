#include <Stepper.h> // библиотека для шагового двигателя


const int stepsPerRevolution = 150;

// устанавливаем порты для подключения драйвера
Stepper myStepper(stepsPerRevolution, 4, A0, 2, 3);

void setup() {
  myStepper.setSpeed(100); // устанавливаем скорость 60 об/мин
}

void loop() {
  // поворачиваем ротор по часовой стрелке
  myStepper.step(stepsPerRevolution);
  delay(2000);
  myStepper.step(-stepsPerRevolution);
  delay(2000);


}
