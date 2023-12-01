/*
  @author: T. Malfatti <malfatti@disroot.org>
  @date: 2018-06-06
  @license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
  @homepage: https://gitlab.com/Malfatti/SciScripts
*/

const int InPinNo = 6;
const int InPins[InPinNo] = {A0, A1, A2, A3, A4, A5};

const int OutPinNo = 8;
const int OutPins[OutPinNo] = {2, 4, 7, 8, 10, 11, 12, 13};
const int OutDelay = 10;

void setup() {
  Serial.begin(115200);
}

void TTLOutput() {
  /*
    Serial-controlled TTL generator. Useful for triggering recordings and/or
    devices.

      A = Pulse on OutPins[0] with duration set in line 30 as `OutDelay`
      B = Pulse on OutPins[1] with duration set in line 30 as `OutDelay`
      C = Pulse on OutPins[2] with duration set in line 30 as `OutDelay`
      D = Pulse on OutPins[3] with duration set in line 30 as `OutDelay`
      E = Pulse on OutPins[4] with duration set in line 30 as `OutDelay`
      F = Pulse on OutPins[5] with duration set in line 30 as `OutDelay`
      G = Pulse on OutPins[6] with duration set in line 30 as `OutDelay`
      P = Pulse on OutPins[7] with duration set in line 30 as `OutDelay`

      a = Keeps OutPins[0] high until z is received
      b = Keeps OutPins[1] high until y is received
      c = Keeps OutPins[2] high until x is received
      d = Keeps OutPins[3] high until w is received
      e = Keeps OutPins[4] high until v is received
      f = Keeps OutPins[5] high until u is received
      g = Keeps OutPins[6] high until t is received
      p = Keeps OutPins[7] high until s is received

      T = Custom protocol (User playground :) )
  */

  char ch = 0;

  while (ch == 0) {
    ch = Serial.read();
  }

  if (ch == 'A') {
    digitalWrite(OutPins[0], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[0], LOW);
  }

  if (ch == 'a') {
    digitalWrite(OutPins[0], HIGH);
    while (ch != 'z') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[0], LOW);
  }


  if (ch == 'B') {
    digitalWrite(OutPins[1], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[1], LOW);
  }

  if (ch == 'b') {
    digitalWrite(OutPins[1], HIGH);
    while (ch != 'y') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[1], LOW);
  }

  if (ch == 'C') {
    digitalWrite(OutPins[2], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[2], LOW);
  }

  if (ch == 'c') {
    digitalWrite(OutPins[2], HIGH);
    while (ch != 'x') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[2], LOW);
  }

  if (ch == 'D') {
    digitalWrite(OutPins[3], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[3], LOW);
  }

  if (ch == 'd') {
    digitalWrite(OutPins[3], HIGH);
    while (ch != 'w') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[3], LOW);
  }

  if (ch == 'E') {
    digitalWrite(OutPins[4], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[4], LOW);
  }

  if (ch == 'e') {
    digitalWrite(OutPins[4], HIGH);
    while (ch != 'v') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[4], LOW);
  }

  if (ch == 'F') {
    digitalWrite(OutPins[5], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[5], LOW);
  }

  if (ch == 'f') {
    digitalWrite(OutPins[5], HIGH);
    while (ch != 'u') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[5], LOW);
  }

  if (ch == 'G') {
    digitalWrite(OutPins[6], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[6], LOW);
  }

  if (ch == 'g') {
    digitalWrite(OutPins[6], HIGH);
    while (ch != 't') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[6], LOW);
  }

  if (ch == 'P') {
    digitalWrite(OutPins[7], HIGH);
    delay(OutDelay);
    digitalWrite(OutPins[7], LOW);
  }

  if (ch == 'p') {
    digitalWrite(OutPins[7], HIGH);
    while (ch != 's') {
      ch = Serial.read();
    }
    digitalWrite(OutPins[7], LOW);
  }

  if (ch == 'T') {
    delay(OutDelay);

    while (true) {
      for (int Pulse = 0; Pulse < 10; Pulse++) {
        digitalWrite(OutPins[7], HIGH); delay(15);
        digitalWrite(OutPins[7], LOW); delay(85);
      }

      digitalWrite(OutPins[7], HIGH); delay(5000);
      digitalWrite(OutPins[7], LOW);
      delay(15000);
    }
  }
}

void ReadAll() {
  /*
    Read digital and analog inputs and print them in serial,
    comma-separated, plus the cpu time in milliseconds.
  */

  Serial.print("D[");
  Serial.print(PINB);
  Serial.print(",");
  Serial.print(millis());
  Serial.print("]");
  for (int Pin = 0; Pin < InPinNo; Pin++) {
    Serial.print("A");
    Serial.print(Pin);
    Serial.print("[");
    Serial.print(analogRead(InPins[Pin]));
    Serial.print(",");
    Serial.print(millis());
    Serial.print("]");
  }
  Serial.print("\r\n");
}

void loop() {
  char ch = 0;
  while (ch == 0) {
    ch = Serial.read();
  }

  if (ch == 'I') {
    analogReference(INTERNAL);

    DDRB =  0b00000000;
    PORTB = 0b00000000;

    for (int Pin = 0; Pin < InPinNo; Pin++) {
      pinMode(InPins[Pin], INPUT);
    }

    while (true) {
      ReadAll();
    }
  }

  if (ch == 'O') {
    for (int Pin = 0; Pin < OutPinNo; Pin++) {
      pinMode(OutPins[Pin], OUTPUT);
      digitalWrite(OutPins[Pin], LOW);
    }

    while (true) {
      TTLOutput();
    }
  }
}
