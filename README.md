# Delfi-PQ - Intergration testing

## Purpose
(Maybe including that subsystems for small satellits do not consist of any additional units other then the ones absolute needed, cannot monitor the execution of the task, only send command and receive replyies, but no guarantee it actually worked.)

Delfi-PQ belongs to the new type of miniaturized satellites, namely PocketQube satellites, which exhibit certain advantages over the widely used CubeSats. Due to their smaller size, PocketQubes bring a decrease in total cost and development time. Following, the main objective of Delfi-PQ is to test the application of a PocketQube satellite for future missions, since it is expected that the reduced development cycle will allow a comparably higher launch frequency, increasing flight experience and reliaility of the system.

To ensure that the respective subsystems are operational the intergration of the Delfi-PQ system is tested. While in space, the functinality of a subsystem can not be observed directly and received positive feedback from the subsystem itself does not guarantee a faultless execution of the specified task. Additionally, the subsystem hardware itself is not able to detect if the execution was in fact successful. Hence, it is necessary to deploy verification through an external hardware if the command given to the subsystem was effectively executed.

This project will focus on the design and implementation of a solution for verifying the successful execution of a command given to the subsystem. In particular, the verification of the LED command to the ??....?? board is demonstarted via external hardware (Arduino mega). The here presented software is intended to be modified easily in order to adapt the intergration testing to different subsystems of the Delfi-PQ.


- receiving feedback from external hardware if the command given to the board was successfully executed
- verification
- when in space no-one can check if the led is actually on
- hard ware itself does not detect if the led is on itself
tests the intergration of the Delfi-PQ system

## Repository overview
Besides this README file, the repository includes following files:
- **arduino_feedback.ino**:
- **blablabla**:
- **blablabla**:

## Design



so i was thinking of having something that says each 5/10 seconds: The LED is ON (like, if serial reads 1, print this)

if the user sets it to off and it's on, it says: Error, output is not what was chosen. Log file saved; then it saves a file with the time, with what was chosen and what it read


tell user what to do
exit programm press control C
use there commands: led on of

get user input
thread 1
use user input
turn on -> turn led on
turn off -> turn led off


thread 2
check arduino serial,
compare to user input


if error
log file will be saved, saves error
and saves comment


### Python block diagram
### Arduino block diagram


## How to use

### Requiered hardware

In order to use the scripts provided in this repository, the user will need following hardware items: 
- **SimpleLink™ MSP432P401R LaunchPad**: Runs python scripts and is simulating the Delfi-PQ subsystem
- **Arduino (UNO, MEGA, ect.)**: Used as the external hardware 
- **Wires and Breadboard**: To connect the LaunchPad and Arduino


### Implementing the software

java file running - as local host

in stall py.serial library  in order to allows communication between python and arduino

run python script 

commend  to open and be in right directory 
libraries

(does this belong into design? no, right?)

When xxx.py is running, the user will be provided with the commands available and a short description thereof:
```
command 1 - blablabla
command 2 - ---------
command 3 - --------
Press Ctrl + C: Exit program
```
Following, the user will provide the subsystem with a command to execute a task, here either 'Turn LED on' or 'Turn LED off'.
...




## Results

## Issues encountered

- the connection between LaunchPad and EGSE is not established: remedy: try until it is


## Future changes and recommendations
instead of connecting to the led can be used to verify the funcionality of another Delfi-PQ subsystem

