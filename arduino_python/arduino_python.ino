String inputString = ""; 

void setup(){
  Serial.begin(57600);
  // tell controller to go ahead
  Serial.print("PY>>>");
}

int i = 0;
char reply[5];
void loop(){
  
  while (Serial.available()) {
    reply[i] = (char)Serial.read();
    Serial.write(reply[i]);
    i++;
  }
  
  
}

