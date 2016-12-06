
#include <VarSpeedServo.h> 

VarSpeedServo myservo1;  // create servo object to control a servo
VarSpeedServo myservo2;  // create servo object to control a servo

// twelve servo objects can be created on most boards


int init_pos1 = 90;    // initial servo position is 78degree, the range is limited in (15-165)
int init_pos2 = 0;    // initial servo position is 15degree, the range is limited in (0-78)                                                                                                                                                                                                                                                50;7777778    // initial servo position is 15degree, the range is limited in (15-105)

void setup() {
  Serial.begin(9600);  // initialize serial:
  myservo1.attach(5);  // attaches the servo on pin 6 to the servo object
  myservo2.attach(6); // attaches the servo on pin 7 to the servo object

  myservo1.write(init_pos1);
  myservo2.write(init_pos2);

}

void loop(){
  while (Serial.available() > 0) {
   int spd = Serial.parseInt(); // looking for the incoming of speed control
   int ang1 = Serial.parseInt(); // looking for the incoming
   int pos1 = 15.6+0.83*ang1;
   int ang2 = Serial.parseInt(); // looking for the incoming
   int pos2 = 0.87*ang2;
 

    if (Serial.read() == '\n') {
      spd = constrain(spd, 0, 2);
      pos1 = constrain(pos1, 0, 165);
      pos2 = constrain(pos2, 0, 78);

      Serial.print(spd);
      Serial.print(ang1);
      Serial.print(ang2);

      if (spd == 0){
        myservo1.write(pos1, 10, false);
        myservo2.write(pos2, 10, false);
         } else if (spd == 1){
        myservo1.write(pos1, 30, false);
        myservo2.write(pos2, 30, false);
         } else if (spd == 2){
        myservo1.write(pos1, 50, true);
        myservo2.write(pos2, 50, true);
      }
  }
}
}


