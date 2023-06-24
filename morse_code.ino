#define LED_PIN 3
#define BUTTON_PIN 2
#define BUZZER_PIN 6
#define DOT_PIN 5
#define DASH_PIN 4

class Morse {
  public:
    const int TABLE_SIZE = 37;
    float unitLength = 500; // milliseconds

    const char *getMorse(char chr) {
      // gets morse code string from character
      int index = getTableIndex(chr);

      return table[index];
    }

    const char getChar(char morseCode[], size_t morseLength=0) {
      // gets character form morse code string
      morseLength = (morseLength == 0) ? strlen(morseCode) : morseLength;

      int index = -1;
      char chr = '\0';

      for(int i = 0; i < TABLE_SIZE; i++) {
        if(strcmp(morseCode, table[i]) == 0) {
          index = i;

          break;
        }
      }

      chr = getIndexChar(index);

      return chr;
    }

  private:
    char dot = '.';
    char dash = '-';
    char space = '/';

    const char table[37][6] = {
      {dot, dash, '\0'},                        // A
      {dash, dot, dot, dot, '\0'},              // B
      {dash, dot, dash, dot, '\0'},             // C
      {dash, dot, dot, '\0'},                   // D
      {dot, '\0'},                              // E
      {dot, dot, dash, dot, '\0'},              // F
      {dash, dash, dot, '\0'},                  // G
      {dot, dot, dot, dot, '\0'},               // H
      {dot, dot, '\0'},                         // I
      {dot, dash, dash, dash, '\0'},            // J
      {dash, dot, dash, '\0'},                  // K
      {dot, dash, dot, dot, '\0'},              // L
      {dash, dash, '\0'},                       // M
      {dash, dot, '\0'},                        // N
      {dash, dash, dash, '\0'},                 // O
      {dot, dash, dash, dot, '\0'},             // P
      {dash, dash, dot, dash, '\0'},            // Q
      {dot, dash, dot, '\0'},                   // R
      {dot, dot, dot, '\0'},                    // S
      {dash, '\0'},                             // T
      {dot, dot, dash, '\0'},                   // U
      {dot, dot, dot, dash, '\0'},              // V
      {dot, dash, dash, '\0'},                  // W
      {dash, dot, dot, dash, '\0'},             // X
      {dash, dot, dash, dash, '\0'},            // Y
      {dash, dash, dot, dot, '\0'},             // Z
      {dash, dash, dash, dash, dash, '\0'},     // 0
      {dot, dash, dash, dash, dash, '\0'},      // 1
      {dot, dot, dash, dash, dash, '\0'},       // 2
      {dot, dot, dot, dash, dash, '\0'},        // 3
      {dot, dot, dot, dot, dash, '\0'},         // 4
      {dot, dot, dot, dot, dot, '\0'},          // 5
      {dash, dot, dot, dot, dot, '\0'},         // 6
      {dash, dash, dot, dot, dot, '\0'},        // 7
      {dash, dash, dash, dot, dot, '\0'},       // 8
      {dash, dash, dash, dash, dot, '\0'},      // 9
      {space, '\0'}                               // space
    };

    int getTableIndex(char chr) {
      // gets index of character in morse code table
      int index;

      if(isalpha(chr)) {
        chr = tolower(chr);

        index = chr - 'a';
      } else if(isdigit(chr)) {
        index = chr - '0' + 26;
      } else if(isspace(chr)) {
        index = TABLE_SIZE - 1;
      }

      return index;
    }

    char getIndexChar(int index) {
      // gets character of index in morse code table
      char chr = '\0';

      if(index <= 25) {
        chr = 'a' + index;
      } else if(index <= 35) {
        chr = '0' + index - 26;
      } else if(index == TABLE_SIZE - 1) {
        chr = ' ';
      }

      return chr;
    }
};

const int buzzerTone = 1000;
const char END_MARKER = '\n';
int bufferLength = 32;
Morse *morse;

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DOT_PIN, OUTPUT);
  pinMode(DASH_PIN, OUTPUT);

  while(!Serial) {;}

  Serial.println("Program start");
  Serial.println("");

  morse = new Morse();
}

void loop() {
  select();
}

const char *inputString(int len=bufferLength) {
  while(Serial.available() == 0) {;}

  char *str = malloc(len);
  char chr;
  int index = 0; // index of current character

  while(true) {
    if (Serial.available() > 0) {
      chr = Serial.read();

      if (chr != END_MARKER) {
          str[index] = chr;
          index++;
          if (index >= len) {
              index = len - 1;
          }
      }
      else {
          str[index] = '\0'; // terminate the string
          break;
      }
    }
  }

  return str;
}

void select() {
  Serial.print("1: english -> morse, 2: morse -> english >");

  char *input = malloc(bufferLength);
  strcpy(input, inputString());
  Serial.println(input);
  
  int selection = atoi(input);

  switch(selection) {
    case 1:
      // english -> morse
      engToMorse();
      break;
    case 2:
      // morse -> english
      morseToEng();
      break;
    default:
      Serial.print(selection);
      Serial.println(" is not a valid option");
  }
}

void engToMorse() {
  char morseCode[6];
  char text[bufferLength];
  
  Serial.println("input english text");
  Serial.print(">");
  strcpy(text, inputString());
  Serial.println(text);

  size_t textLength = strlen(text);
  size_t morseLength;

  for(int i = 0; i < textLength; i++) {
    strcpy(morseCode, morse->getMorse(text[i]));

    morseLength = strlen(morseCode);

    for(int j = 0; j < morseLength; j++) {
      Serial.print(morseCode[j]);
      sendSignal(morseCode[j]);

      delay(morse->unitLength);
    }
    Serial.print(" ");

    delay(morse->unitLength*3);
  }

  Serial.println();
}

void morseToEng() {
  Serial.print("1: keyboard input, 2: button input, 9: back >");

  char *input = malloc(bufferLength);
  strcpy(input, inputString());
  Serial.println(input);
  
  int selection = atoi(input);

  switch(selection) {
    case 1:
      // keyboard input
      morseToEngKeyboard();
      break;
    case 2:
      // button input
      morseToEngButton();
      break;
    case 9:
      // back
      break;
    default:
      Serial.print(selection);
      Serial.println(" is not a valid selection");
  }
}

void sendSignal(char chr) {
  if(chr == '/') {
    // there are 3 unit delays before and after the space so only 1 unit delay here
    delay(morse->unitLength);
  } else {
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, buzzerTone);

    if(chr == '.') {
      digitalWrite(DOT_PIN, HIGH);

      delay(morse->unitLength);
    } else if(chr == '-') {
      digitalWrite(DASH_PIN, HIGH);

      delay(morse->unitLength*3);
    }

    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);

    digitalWrite(DOT_PIN, LOW);
    digitalWrite(DASH_PIN, LOW);
  }
}

void morseToEngKeyboard() {
  char morseCode[bufferLength*6];
  char text[bufferLength];

  Serial.println("input morse code with keyboard");
  Serial.println("Ex) .... . .-.. .-.. --- / .-- --- .-. .-.. -.. => Hello World (spaces are important)");
  Serial.print(">");

  strcpy(morseCode, inputString(bufferLength*6));
  Serial.println(morseCode);

  strcpy(text, morseStringToEng(morseCode));

  Serial.println(text);
  Serial.println();
}

void morseToEngButton() {
  char morseCode[bufferLength*6];
  char text[bufferLength];

  strcpy(morseCode, inputMorseButton());

  strcpy(text, morseStringToEng(morseCode));

  Serial.println(text);
  Serial.println();
}

const char *morseStringToEng(char morseCode[]) {
  size_t morseLength = strlen(morseCode);
  int morseCount = 0, textCount = 0;

  char *text = malloc(bufferLength);
  char morseCharacter[6] = "";

  morseCode[morseLength] = ' ';
  morseCode[++morseLength] = '\0';

  for(int i = 0; i < morseLength; i++) {
    if(morseCode[i] == ' ') {
      morseCharacter[morseCount] = '\0';
      text[textCount] = morse->getChar(morseCharacter);

      morseCount = 0;
      textCount++;
    } else if(morseCode[i] == '/') {
      text[textCount] = ' ';

      textCount++;
      i++;
    } else {
      morseCharacter[morseCount] = morseCode[i];

      morseCount++;
    }

    if(textCount >= bufferLength) {
      textCount = bufferLength-1;
    }
  }

  text[textCount] = '\0';

  return text;
}

const char *inputMorseButton() {
  char *morseCode = malloc(bufferLength*6);

  int morseCount = 0;
  int buttonState;
  int loopCount = 0;
  int delayLength = 10;
  int unitsPerDelay = morse->unitLength / delayLength;
  boolean first = true;

  Serial.println("input morse code with button");
  Serial.print(">");

  while(true) {
    loopCount = 0;
    
    buttonState = digitalRead(BUTTON_PIN);

    while(buttonState == LOW) {
      if(first == false && loopCount > unitsPerDelay*15) {
        break;
      }

      buttonState = digitalRead(BUTTON_PIN);
      loopCount++;

      delay(delayLength);
    }

    if(first) {
      loopCount = 0;
      first = false;
    } else {
      first = false;

      if(loopCount <= unitsPerDelay*3) { // is space between morse symbols so don't output anything
        ;
      } else if(loopCount <= unitsPerDelay*7) { // space between letters
        morseCode[morseCount] = ' ';
        Serial.print(' ');
        Serial.flush();

        morseCount++;
      } else if(loopCount <= unitsPerDelay*15) { // space between words
        morseCode[morseCount] = ' ';
        morseCode[morseCount+1] = '/';
        morseCode[morseCount+2] = ' ';
        Serial.print(" / ");
        Serial.flush();

        morseCount += 3;
      } else { // longer than unitsPerDelay*15 is quitting
        break;
      }
    }

    loopCount = 0;

    while(buttonState == HIGH) {
      if(loopCount <= unitsPerDelay*2) {
        digitalWrite(DOT_PIN, HIGH);
      } else if(loopCount <= unitsPerDelay*7) {
        digitalWrite(DOT_PIN, LOW);
        digitalWrite(DASH_PIN, HIGH);
      } else {
        break;
      }

      buttonState = digitalRead(BUTTON_PIN);
      tone(BUZZER_PIN, buzzerTone);
      digitalWrite(LED_PIN, HIGH);

      loopCount++;

      delay(delayLength);
    }

    noTone(BUZZER_PIN);
    digitalWrite(LED_PIN, LOW);
    digitalWrite(DOT_PIN, LOW);
    digitalWrite(DASH_PIN, LOW);

    if(loopCount <= unitsPerDelay*2) { // dot
      morseCode[morseCount] = '.';
      Serial.print('.');
      Serial.flush();

      morseCount++;
    } else if(loopCount <= unitsPerDelay*7) { // dash
      morseCode[morseCount] = '-';
      Serial.print('-');
      Serial.flush();

      morseCount++;
    } else { // quit
      break;
    }
  }

  morseCode[morseCount] = '\0';
  Serial.println();

  return morseCode;
}