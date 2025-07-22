
#include <Keypad.h>

const byte ROWS= 4; //number of rows on the keypad
const byte COLS= 4; //number of columns on the keypad


char keymap[ROWS][COLS]=
{
{'1', '2', '3', 'A'},
{'4', '5', '6', 'B'},
{'7', '8', '9', 'C'},
{'*', '0', '#', 'D'}
};


byte rowPins[ROWS] = {9,8,7,6}; 
byte colPins[COLS] = {5,4,3,2}; 

Keypad myKeypad = Keypad(makeKeymap(keymap), rowPins, colPins, ROWS, COLS);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  char keypressed = myKeypad.getKey();
  if (keypressed)
    {
      Serial.println(keypressed);
    }
}
