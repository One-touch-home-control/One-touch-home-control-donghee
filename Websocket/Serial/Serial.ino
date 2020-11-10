#define LED_PIN 13

String input = "";
int isOnLED = 0;
void setup(){
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ready");
}

 
void loop(){
  
  while(!Serial.available());
  input = Serial.readStringUntil('\n');
  if(input == "led")
  {
    if(isOnLED == 0){
      digitalWrite(LED_PIN, HIGH);
      isOnLED = 1;
    }
    else{
      digitalWrite(LED_PIN, LOW);
      isOnLED = 0;
    }
    Serial.println(input);
  }
  else{
    Serial.println("error");
  }
}
