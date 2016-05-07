#include <Wire.h>
#include <SoftwareSerial.h>
#include <Password.h> //http://www.arduino.cc/playground/uploads/Code/Password.zip
#include <Keypad.h> //http://www.arduino.cc/playground/uploads/Code/Keypad.zip
#include <LiquidCrystal.h>
#include <Servo.h>
int led=A1;
#define led A1
#define Led A2;
#define pouss A3;
int A=0;



Servo myservo;
LiquidCrystal lcd(13,12,4,3,2,1);
Password password = Password( "1234" );

const byte ROWS = 4; // Four rows
const byte COLS = 3; //  columns
int i=11;
int nbErreur=0;
// Define the Keymap
char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = { 8,7,6,5 };// Connect keypad ROW0, ROW1, ROW2 and ROW3 to these Arduino pins.
byte colPins[COLS] = { 11,10,9 };// Connect keypad COL0, COL1 and COL2 to these Arduino pins.


// Create the Keypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup(){
   pinMode(A1,OUTPUT);
   pinMode(A2,OUTPUT);
   pinMode(A3,INPUT);
   lcd.begin(16,2);
   lcd.setCursor(0,0);
   lcd.print("hello!");
   delay(50);
   keypad.addEventListener(keypadEvent); //add an event listener for this keypad
   myservo.attach(A0);
   myservo.write(90);
}

void loop(){
  keypad.getKey();
}

//take care of some special events
void keypadEvent(KeypadEvent eKey){
  
  switch (keypad.getState()){
    case PRESSED:
         lcd.setCursor(0,0);
	lcd.print("Code:");
        lcd.setCursor(i,0);
        if (eKey!='#')
        	lcd.print('*');//eKey);*
        i++;

	switch (eKey){
	  case '*': checkPassword(); break;
	  case '#': password.reset();lcd.clear(); break;
	  default: password.append(eKey);
     }
  }
}

void checkPassword(){
  lcd.clear();
  if(nbErreur<3){
    if (password.evaluate()){
      lcd.setCursor(1,1);
      lcd.print("Access");
     myservo.write(90);
     digitalWrite(A1,HIGH);
      //delay(60000);
      myservo.write(180);
          //Add code to run if it works
    }else{
      lcd.setCursor(1,3);
      lcd.print("Erreur");
      digitalWrite(A1,LOW);
      lcd.clear();
      lcd.setCursor(1,0);
      lcd.print("tentative");
      lcd.setCursor(1,1);
      lcd.print(3-nbErreur);
      nbErreur++;
      //add code to run if it did not work
    }
    i=11;
  }
  else{
    Alarme();
  }
}


void Alarme(){
  lcd.clear();
    lcd.setCursor(0,1);
    lcd.print("Alarme");
    A=digitalRead(pouss);
    if(A==LOW)
    {
      digitalWrite(A2,HIGH);
      delay(1000);
     digitalWrite(A2,LOW);
     delay(1000);
   }
    else
    {
      digitalWrite(A2,LOW); 
     }  
   }
   nbErreur=0;
}
