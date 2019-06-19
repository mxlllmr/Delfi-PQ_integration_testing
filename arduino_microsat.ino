int testpin = 7;
int value = 0;
//int k = 0;


void setup() {
  // Uncomment the prints, k variable and k++ to debug
  Serial.begin(9600);
  //Serial.print("Hello, I'm here to verify if everything is working as it should (:"); Serial.print( '\n');
  pinMode(testpin, INPUT);
}

void loop() {
  //k++;
  value = digitalRead(testpin);
  
  // Serial.print("This is loop number: "); Serial.print(k); Serial.print( '\n'); 
  // Serial.print("Your INPUT is:"); Serial.print( '\n'); 
  Serial.print(value); Serial.print( '\n');
  delay(1000);
}
