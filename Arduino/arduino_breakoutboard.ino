//adapted from 'X9C103P Basic Operation' https://www.instructables.com/id/X9C103P-Basic-Operation/

#define ANALOG_REFERENCE 5.0
#define POT_VALUE 10000         // Nominal POT value
#define STEP_OHMS POT_VALUE/100 // Number of ohms per tap point
#define PULSE_TIME 10           

const int pinUD = 8;            // --> X9C103P pin 2
const int pinINC = 9;           // --> X9C103P pin 1
const int pinCS = 10;           // --> X9C103P pin 7
const int pinWiper = A1;        // --> X9C103P pin 5 for analoge read

const int tap_low = 100;
const int tap_mid = POT_VALUE/2;
const int tap_high = POT_VALUE;
int sampleADC = 0;
float voltage = 0;
float ohm = 0;
float law = 0;
int wiper = 0;

void setup() {
  // Set up digital pins
  pinMode (pinCS, OUTPUT);
  digitalWrite(pinCS,HIGH);        //deselect the POT
  pinMode (pinUD, OUTPUT); 
  pinMode (pinINC, OUTPUT);
  // Set analog pin to known state just to be thorough
  pinMode(pinWiper, INPUT);
  digitalWrite(pinWiper, LOW);
  
  // Invoke the serial communicatiom
  Serial.begin(9600);
  digitalWrite(pinCS,HIGH);     //deselect the POT
  
  // uncommend all 'Serial.print()' if monitor output is wanted
  
  //Serial.println("\n* X9C103P Basic Operation Loop *\n");
  //Serial.print("\n* Choose '1' for low, '2' for medium or '3' for high. *\n");

  // Setup state
  ohm = tap_low;
  digitalWrite(pinUD, LOW);
  voltage = g_PrintADC(pinWiper);
  law = (POT_VALUE)*(voltage/ANALOG_REFERENCE);
  //Serial.print( '\n');
  //Serial.print("   law = "); Serial.println(law); Serial.print( '\n');
  for (int i = 0; i < 127; i++)
  {
    X9C103P_INC(pinCS,pinINC);
    delay(1);
  }
}

void loop() {

  if (Serial.available() > 0) {
     char input = Serial.read();
     //Serial.print(input);

   // choose 1,2,3 for low medium or high value

  if (input == '1') {
       ohm = tap_low;
       digitalWrite(pinUD, LOW);
       //Serial.print("   Ohm = "); Serial.println(ohm);
       voltage = g_PrintADC(pinWiper);
       law = (POT_VALUE)*(voltage/ANALOG_REFERENCE);
       //Serial.print( '\n');
       //Serial.print("   law = "); Serial.println(law); Serial.print( '\n');
       for (int i = 0; i < 127; i++){
       X9C103P_INC(pinCS,pinINC);
       delay(1);
       }
       wiper = 0;
  }
  else if (input == '2') {
      if (wiper == 0){
      digitalWrite(pinUD, HIGH);
     }
      else  if (wiper == 1){
      digitalWrite(pinUD, LOW);
     }
      if (wiper != 2){ 
       ohm = tap_mid;
       //Serial.print("   Ohm = "); Serial.println(ohm);
       voltage = g_PrintADC(pinWiper);
       law = (POT_VALUE)*(voltage/ANALOG_REFERENCE);
       //Serial.print( '\n');
       //Serial.print("   law = "); Serial.println(law); Serial.print( '\n');
       for (int i = 0; i < 50; i++){
       X9C103P_INC(pinCS,pinINC);
       delay(1);
       }
       wiper = 2;
       }
  }
  else if (input == '3') {
       digitalWrite(pinUD, HIGH);
       ohm = tap_high;
       //Serial.print("   Ohm = "); Serial.println(ohm);
       voltage = g_PrintADC(pinWiper);
       law = (POT_VALUE)*(voltage/ANALOG_REFERENCE);
       //Serial.print( '\n');
       //Serial.print("   law = "); Serial.println(law); Serial.print( '\n');
       for (int i = 0; i < 127; i++){
       X9C103P_INC(pinCS,pinINC);
       delay(1);
       }
       wiper = 1;     
  }  
  else  { 
    }}
}

void X9C103P_INC(int enable, int pulse){

  digitalWrite(pulse, HIGH);   // HIGH before falling edge 
  delay(PULSE_TIME);           // wait for IC/stray capacitance ?
  digitalWrite(enable,LOW);    // select the POT
  digitalWrite(pulse, LOW);    // LOW for effective falling edge
  delay(PULSE_TIME);           // wait for IC/stray capacitance ?
  digitalWrite(enable,HIGH);   //deselect the POT 
}

float g_PrintADC(byte anaPin)
{
  int sampleADC = analogRead(anaPin);
  float volts = (sampleADC * ANALOG_REFERENCE)/ 1023.0;
  //Serial.print("   ADC = ");
  //Serial.print(sampleADC);     
  //Serial.print("\tVoltage = ");
  //Serial.print(volts,3);
  return volts;
}
