#include <Servo.h>

// создаём объекты для управления сервоприводами
Servo myservo1;
Servo myservo2;

void setup()
{
  // подключаем сервоприводы к выводам 11 и 12
  myservo1.attach(10);
  myservo2.attach(9);
}

void loop()
{
  // устанавливаем сервоприводы в серединное положение
  myservo1.write(0);
  myservo2.write(0);

}
