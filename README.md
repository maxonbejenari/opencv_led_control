# Opencv_led_control

## Create a directory
```
mkdir name_of_dir
cd name_of_dr
```

## Clone repo
```bash
git clone https://github.com/maxonbejenari/opencv_led_control
```

## Create a venv
```bash
pythin3 -m venv name_of_venv
source name_of_venv/bin/activate
```

## PIP
```bash
pip install -r /path/to/requirements.txt
```

## Arduino code
```bash
#include <Arduino.h>

const uint8_t led_pin = 11;

void setup() {
  Serial.begin(9600);
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');
    int command = incoming.toInt();

    if (command == 0) {
      digitalWrite(led_pin, LOW);
    } else {
      digitalWrite(led_pin, HIGH);
    }
  }
}
```
