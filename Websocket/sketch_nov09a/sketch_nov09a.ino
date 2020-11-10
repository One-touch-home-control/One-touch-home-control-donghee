//#define no_dust 0.3
//#define dustout A0
//#define v_led 8
//
//void setup(){
//  Serial.begin(9600);
//  pinMode(v_led, OUTPUT);
//  pinMode(dustout, INPUT);
//}
//
//int r = 1;
//float dust_density = 0;
//void loop(){
//  digitalWrite(v_led, LOW);
//  delayMicroseconds(280);
//  float vo_value = analogRead(dustout);
//  delayMicroseconds(40);
//  digitalWrite(v_led, HIGH);
//  delayMicroseconds(9680);
//  
//  Serial.println(vo_value);
//  if(Serial.available()){
//    r = r + (Serial.read() - '0');
//  }
//  delay(1200);
// }
// 
// float get_voltage(float value){
//   return value * 5.0 / 1024.0;
// }
// float get_dust_density(float voltage){
//   return (voltage - no_dust) / 0.005;
// }

int Vo = 14;
int V_LED = 2;

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

void setup(){
  Serial.begin(9600);
  pinMode(V_LED, OUTPUT);
  pinMode(Vo, INPUT);
}

void loop(){
  digitalWrite(V_LED, LOW);
  delayMicroseconds(280);
  Vo_value = analogRead(Vo);
  delayMicroseconds(40);
  digitalWrite(V_LED, HIGH);
  delayMicroseconds(9680);

  Voltage = Vo_value * 5.0/1024.0;
  dustDensity = (Voltage - 0.3) / 0.005;
  
//  Serial.print("volatage: ");
//  Serial.println(Voltage);
//  Serial.print("dustDensity: ");
  Serial.print("start");
  Serial.print((int)dustDensity);
  Serial.println("end");
  
  delay(100);
}
