# Delfi-PQ - Integration testing

## Purpose

Delfi-PQ belongs to the new type of miniaturized satellites, namely PocketQube satellites, which exhibit certain advantages over the widely used CubeSats. Due to their smaller size, PocketQubes bring a decrease in total cost and development time. The main objective of Delfi-PQ is to test the application of a PocketQube satellite for future missions since it is expected that the reduced development cycle will allow a comparably higher launch frequency, increasing flight experience and reliability of the system.

To ensure that the respective subsystems are operational, the integration of the Delfi-PQ system must be tested. While in space, the functionality of a subsystem cannot be observed directly and positive feedback from the subsystem itself does not guarantee a faultless execution of the specified task. Additionally, the subsystem hardware itself is not able to detect if the execution was in fact successful. Hence, it is necessary to deploy verification through external hardware if the command given to the subsystem was effectively executed.

This project will focus on the design and implementation of a solution for verifying the successful execution of a command given to the subsystem. In particular, the verification of the LED command to the LaunchPad (Texas Instruments) is demonstrated via external hardware (Arduino Mega). Thereafter, the same logic is applied in order the verify the power bus command to the ADB of Delfi-PQ. The provided software is intended to be modified easily in order to adapt the integration testing to different subsystems of the Delfi-PQ.

## Repository overview
Besides this README file, the repository includes the following files:
- **arduino_feedback.ino**: Arduino script that must be uploaded to the Arduino board
- **client_LED.py**: Python script with UI to change the state of the LED
- **client_ADB.py**: Python script with UI to change the state of the ADB (Antenna Deployment Board) power bus
- **client_ADB_noUI.py**: Python script without UI to change the state of the ADB power bus
- **pq_comms.py**: Python script that converts the commands of the client scripts into messages that are sent to the board

Additionally, the remaining necessary files (that were not created or modified by us) are included, such as:
- **pq_module.py**
- **EGSE software**: in the folder "PQ9EGSE-master"

## Literature background

### Integration testing

### ADB

## Design

The overall purpose of this project is to do integration testing of the Delfi-PQ subsystems. To do so, first the interaction between the PC and a SimpleLink™ MSP432P401R LaunchPad, which emulates the on-board software, is tested. This is done by plugging an Arduino to the PC and connect one of its GPIO ports to the LaunchPad. This way the commands are tested both with the subsystem feedback (either by printing it in the terminal or by using the EGSE software) and with the external hardware feedback.

### Arduino 

The Arduino script is the simplest one. It updates every second in the Serial Monitor the value that is read in the GPIO that is connected to the LaunchPad. The Serial Monitor is later interpreted by the python scripts, which in their turn use such values.

#### Arduino block diagram

<img src="https://user-images.githubusercontent.com/50111548/59805326-d0b08800-92a5-11e9-8e63-e66b61d4de22.jpg" width="700"/>

### Python

The script shown below is more complex and requires a more detailed analysis. This is exposed right after it.

#### Python block diagrams


<img src="https://user-images.githubusercontent.com/50111548/59874054-3c502f00-9352-11e9-94ac-8f936c11a446.jpg"/>

- Go through the points in the blocks
(...)


## How to use
The required hard- and sorftware needed to execute the scripts found in this repository are listed below. Further, it is explained in detail how to use the scripts.

### Required hardware

In order to use the scripts provided in this repository, the user will need the following hardware items: 
- **SimpleLink™ MSP432P401R LaunchPad**: Communicates with the python scripts and is simulating the Delfi-PQ subsystem
- **Arduino (UNO, MEGA, etc.)**: Used as the external hardware 
- **Wires**: To connect the LaunchPad and Arduino (2x female/male) and to connect the ADB to the Arduino (2x male/male)


### Software implementation
To run the following software, Arduino IDE, Python 2x and Java must be installed in the user's PC. This software must be cloned or forked there as well.

#### ```arduino_microsat.ino```

To run any of the python scripts, this code must be uploaded to the Arduino board connected to the PC. After checking the connection in Arduino IDE (by choosing the type of board in ```Tools->Board``` and the port in ```Tools->Port```), the user can upload the code to the board.

The Serial Monitor can be checked to verify its normal functioning. To help with this verification, the user can even uncomment the commented lines, as it is indicated in the source code. Nevertheless, to run the python scripts, it is crucial that:
- The Serial Monitor only receives 1 or 0;
- The Serial Monitor is not opened while running the scripts, such that a double access does not happen and interfere with the readings. It is advised that, after the verification of the functionality of this code, Arduino IDE is closed.

#### ```client_LED.py```

#####  Hardware setup
After connecting the Launchpad and the  Arduino to the host computer via USB ports both need to be connected with each other as is shown in the picture below. The GND (ground) pins of both boards need to be connected, as well as the pin P1.0 of the Launchpad's LED1 to the pin 7 on the Arduino board. If another pin instead of pin 7 is prefered the respective pin number has to be modifiued in ```arduino_feedback.ino``` and the software needs to be compiled and uploaded to the Arduino as explained before.

<img src="https://user-images.githubusercontent.com/51790860/59844570-84278400-935b-11e9-9541-93f04d25ead1.jpg" width="400"/>

##### Running ```client_LED.py```

- Libraries needed: ```numpy```, ```serial```, ```threading```, ```sys```, ```time```, ```signal```, ```logging```, ```json```, ```socket```

- Files needed in repository: ```pq_module.py```, ```pq_comms.py```

- Commands: 
  - **0,1,2,... followed by ENTER**: Chooses the Arduino port
  - **0/1 followed by ENTER**: Sends a command to turn OFF/ON the LED
  - **CTRL+c followed by ENTER**: Exits the program
  
In order to run ```client_LED.py``` several steps need to be executed.
1. Run the EGSE software. This Java software should be in a local folder, and it runs by writing:
```
sudo java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar
```
in the terminal.

2. Choose the LaunchPad port in the EGSE software. this done by opening the browser in ```localhost:8080``` and choosing the port as in the picture below:

<img src="https://user-images.githubusercontent.com/50111548/59802762-82e45180-929e-11e9-88b3-2b25fda94401.JPG" width="700"/>

By trial and error, the user can choose a port and verify if it is the correct one by pinging to the DEBUG and verifying a response in the DataLog.

3. Run the python script as:
```
sudo python client_LED.py localhost:8080
```
*NOTE: The last two commands (to run the EGSE and to run the python script) should be executed with the terminal running in the respective folders where the invoked files/paths exist. Else, simply replacing the files names by the full directory should suffice.*

4. After running ```client_LED.py```  a welcome message appears and an explanaition on how to utilise the program, including the commands which can be used:

```
#################################################################
Welcome to the LED detection software!
This application prints out every 10 seconds the Arduino feedback
The commands are: 1 to turn the LED ON, 0 to turn it OFF.
To exit the application press 'CTRL+C'
#################################################################
```
<img src="https://user-images.githubusercontent.com/51790860/59845077-c43b3680-935c-11e9-8ae2-82f78351f9d5.jpg"/>

Thereafter the user is asked to choose the Arduino port
```
Insert the arduino port (0,1,2,...): 
```
Here the port that connects the Arduino to the CPU has to be selected.

*NOTE: The Arduino board has to be connected in the format of ```/dev/ttyACM(...)```, else the program does not recognise it. In case the connection to the PC has a different designation, change line 267 of ```client_LED.py``` to the specific designation (for example, ```COM(...)```)*

If a wrong port was selected the user is notified and asked to try again.

<img src="https://user-images.githubusercontent.com/51790860/59844789-fef09f00-935b-11e9-9907-858408ba19a2.jpg"/>

5. If the connection is established, the program will attempt to connect to the LaunchPad board. This is represented by a progress bar that looks like the following:
```
[###       ]
```
Each ```#``` represents a successful ping with the DEBUG subsystem of the board. 

6. Finally, the program is ready to take commands to turn ON and OFF the LED. Every 10 seconds (after the first user input) an update on the Arduino feedback is printed on the screen. Every time a user inputs 1/0 (+ENTER), the message that is sent to the board is printed. If there is feedback from the board, the following should appear:
```
Command received in DEBUG
```
<img src="https://user-images.githubusercontent.com/51790860/59845344-7246e080-935d-11e9-8a48-4ca8116ef08b.jpg"/>

Additionally, an immediate Arduino feedback check is performed. If the Arduino agrees with the subsystem feedback 
```
Arduino: The LED is ON.
```
is displayed if the LED is turned on and
```
Arduino: The LED is OFF.
```
if the LED is turned off.

<img src="https://user-images.githubusercontent.com/51790860/59845389-94406300-935d-11e9-8232-4000b9af8d01.jpg"/>

Anytime the Arduino disagrees with the subsystem feedback, the user is notified, an ERROR message is saved in an external log_LED.log file and the LED input is set to the according value.

<img src="https://user-images.githubusercontent.com/51790860/59845420-a91cf680-935d-11e9-9df6-bac610be8d8e.jpg"/>

Log file:
<img src="https://user-images.githubusercontent.com/51790860/59852252-be4e5100-936e-11e9-86eb-d327389ba4a6.JPG"/>

8. To exit the program press ```CTRL+C``` (+ENTER).

<img src="https://user-images.githubusercontent.com/51790860/59845518-e41f2a00-935d-11e9-95b7-cf7b989f8c35.jpg"/>

*FINAL REMARKS: This program is protected such that if any undesired input exists, a 'try again' type of notification is printed; The ```ENTER``` command after ```CTRL+c``` is required because there is an existing thread that contains the function ```input()``` that stalls the program. The waiting period is demanded such that existing ```time.sleep()``` functions cease.*

#### ```client_ADB.py```

#####  Hardware setup
Similar as before The Arduino and ADB subsystem need to be connected after both have beenconnected to the host computer via the USB ports. The image below shows the wiring necessary. The GND (ground) pins of both boards need to be connected, as well as the pin belonging to the respective power bus of the ADB (U1, U2, U3, or U4) that is selected for testing to the pin 7 on the Arduino board. As before, if another pin instead of pin 7 is prefered the respective pin number has to be modifiued in ```arduino_feedback.ino``` and the software needs to be compiled and uploaded to the Arduino as explained before. 

<img src="https://user-images.githubusercontent.com/51790860/59849455-f8682480-9367-11e9-863c-5a4f44432d0d.jpg" width="600"/>

##### Running ```client_ADB.py```

- Libraries needed: ```numpy```, ```serial```, ```threading```, ```sys```, ```time```, ```signal```, ```logging```, ```json```, ```socket```

- Files needed in repository: ```pq_module.py```, ```pq_comms.py```

- Commands: 
  - **0,1,2,... followed by ENTER**: Chooses the Arduino port
  - **1,2,3,4 followed by ENTER**: Choose one of the four the ADB power busses
  - **0/1 followed by ENTER**: Sends a command to turn OFF/ON the LED
  - **CTRL+c followed by ENTER**: Exits the program
  
In order to run ```client_ADB.py``` similar steps as in ```client_LED.py``` need to be executed.
1. Before running the EGSE software, delete line 1444 of the ```EPS.xml``` and execute the EGSE software as before by writing:
```
sudo java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar 
```
in the terminal. Alternatively, the in the repository given file ```EPS_ADB.xml``` can be used, when ......... **cannot find it, but it was written here somewhere**

2. Choose the ADB port in the EGSE software as explained under point **2** of **Running ```client_LED.py```**.

<img src="https://user-images.githubusercontent.com/51790860/59848262-fea8d180-9364-11e9-915a-df896b8bb056.JPG" width="700"/>

3. Run the python script as:
```
sudo python client_ADB.py localhost:8080
```
*NOTE: The last two commands (to run the EGSE and to run the python script) should be executed with the terminal running in the respective folders where the invoked files/paths exist. Else, simply replacing the files names by the full directory should suffice.*

4. After running ```client_ADB.py``` a welcome message appears and an explanaition on how to utilise the program, including the commands which can be used:

```
#################################################################
Welcome to the ADB Power Bus verification software!
This application prints out every 10 seconds the Arduino feedback
Choose one of the four busses with 1 for Bus1SW, 2 for Bus2SW, 3 for Bus3SW, or 4 for Bus4SW
The commands are: 1 to turn the BUS ON, 0 to turn it OFF.
To exit the application press 'CTRL+C'
#################################################################
```
<img src="https://user-images.githubusercontent.com/51790860/59848818-627fca00-9366-11e9-8a36-2e139a51f9ab.jpg"/>

The user is asked again to choose the Arduino port.
```
Insert the arduino port (0,1,2,...): 
```
Here the port that connects the Arduino to the CPU has to be selected.

*NOTE: The Arduino board has to be connected in the format of ```/dev/ttyACM(...)```, else the program does not recognise it. In case the connection to the PC has a different designation, change line 271 of ```client_ADB.py``` to the specific designation (for example, ```COM(...)```)*

5. If the connection to the Arduino is established, the program will attempt to connect to the ADB. This is represented by a progress bar that looks like the following:
```
[###       ]
```
Each ```#``` represents a successful ping with the ADB. 

6. Now the application is ready for the bus input. The user is asked to select the connected ADB bus and press ENTER.

<img src="https://user-images.githubusercontent.com/51790860/59848929-a5da3880-9366-11e9-9276-b90ad80ef7f3.jpg"/>

7. After the bus number has been selected, the program is ready to take commands to turn the power bus ON and OFF. Every 10 seconds (after the first user input) an update on the Arduino feedback is printed on the screen. Every time a user inputs 1/0 (+ENTER), the message that is sent to the board is printed. If there is feedback from the board, the following should appear:
```
Command received in DEBUG
```
Additionally, an immediate Arduino feedback check is performed. If the Arduino agrees with the subsystem feedback 
```
Arduino: The BUS Bus1Sw is ON.
```
is displayed if power bus 1 is turned on and
```
Arduino: The BUS Bus1Sw is OFF.
```
if power bus 1 is turned off.

<img src="https://user-images.githubusercontent.com/51790860/59849010-d91cc780-9366-11e9-9522-e7ee45a3ab8f.jpg"/>

Anytime the Arduino disagrees with the subsystem feedback, the user is notified, an ERROR message is saved in an external log_BUS.log file and the BUS input is set to the according value.

<img src="https://user-images.githubusercontent.com/51790860/59849196-40d31280-9367-11e9-9887-ff10f9091f4f.jpg"/>

Log file:
<img src="https://user-images.githubusercontent.com/51790860/59852474-33ba2180-936f-11e9-89f8-a94c37779991.JPG"/>

8. To exit the program press ```CTRL+C``` (+ENTER) as before.

#### ```client_ADB_noUI.py```
#####  Hardware setup
Refer to the hardware setup section of **```client_ADB.py```**.

##### Running ```client_ADB_noUI.py```

- Libraries needed: ```numpy```, ```serial```, ```threading```, ```sys```, ```time```, ```signal```, ```logging```, ```json```, ```socket```

- Files needed in repository: ```pq_module.py```, ```pq_comms.py```

- Commands: 
  - **0,1,2,... followed by ENTER**: Chooses the Arduino port
  - **CTRL+c followed by ENTER**: Exits the program
  
In order to run ```client_ADB_noUI.py``` similar steps as in ```client_ADB.py``` need to be executed.
1. Before running the EGSE software, delete line 1444 of the ```EPS.xml``` and execute the EGSE software as before by writing:
```
sudo java -jar target/PQ9EGSE-0.1-SNAPSHOT-jar-with-dependencies.jar 
```
in the terminal. If the line 1444 has already been deleted, no further action is necessary. Alternatively, the in the repository given file ```EPS_ADB.xml``` can be used, when ......... **cannot find it, but it was written here somewhere**

2. Choose the ADB port in the EGSE software as explained under point **2** of **Running ```client_LED.py```**.

3. Run the python script as:
```
sudo python client_ADB_noUI.py localhost:8080
```
*NOTE: The last two commands (to run the EGSE and to run the python script) should be executed with the terminal running in the respective folders where the invoked files/paths exist. Else, simply replacing the files names by the full directory should suffice.*

4. After running ```client_ADB_noUI.py``` a welcome message appears and an explanaition on how to utilise the program, including the commands which can be used:

```
#################################################################
Welcome to the ADB Power Bus verification software!
Ten ping commands are sent to the ADB.
After that, Bus1SW will be turned ON and turned OFF.
All occuring ERRORS will be logged in log_BUS_noUI.
To exit the application press 'CTRL+C'
#################################################################
```
*NOTE: If instead of Bus 1 (Bus1SW) the bus number needs to be changed at the appropriate locations in ```client_ADB_noUI.py``` (use the search function).

<img src="https://user-images.githubusercontent.com/51790860/59850380-6a416d80-936a-11e9-8099-8e6e3ce1b2f9.jpg"/>

The user is asked again to choose the Arduino port
```
Insert the arduino port (0,1,2,...): 
```
Here the port that connects the Arduino to the CPU has to be selected.

*NOTE: The Arduino board has to be connected in the format of ```/dev/ttyACM(...)```, else the program does not recognise it. In case the connection to the PC has a different designation, change line 238 of ```client_ADB_noUI.py``` to the specific designation (for example, ```COM(...)```)*

5. If the connection to the Arduino is established, the program will attempt to connect to the ADB. This is as before represented by a progress bar that looks like the following:
```
[###       ]
```
Each ```#``` represents a successful ping with the ADB. 10 pings are sent. If a ping was unsuccessfully sent it is saved in the external 'log_BUS_noUI.log file.

<img src="https://user-images.githubusercontent.com/51790860/59852633-7e3b9e00-936f-11e9-8d9a-1010bab32584.JPG"/>

6. Now the user is informed about the following steps of the progam. Bus 1 will be turned ON and OFF and the Arduino feedback check is performed after each command is sent. The displayed output is the same as seen under point **7** of ```client_ADB.py```). After the commands have been performed the program exits automatically.

<img src="https://user-images.githubusercontent.com/51790860/59851296-8e9e4980-936c-11e9-9d07-0ebbdfb3f5b4.jpg"/>

If the Arduino disagrees with the subsystem feedback, the user is notified and an ERROR message is saved in the external log_BUS_noUI.log file with the same output as in ```client_ADB.py```.

## Results

- Show the python scripts running and giving prints. Show log file

- Also put a log file in the repository

## Issues encountered

- The connection between LaunchPad and EGSE was not always established. The only remedy was to kill the EGSE instance and rerun it until it worked.

- The LaunchPad LED P1.0 GPIO connection burned and the LED was constantly ON when plugged in. This was remedied by manually connecting/disconnecting the cable accordingly (or not) to the user input.


## Future changes and recommendations
- Instead of connecting to the LED, this can be used to verify the funcionality of another Delfi-PQ subsystem

- ? We need more

