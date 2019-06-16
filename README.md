# Delfi-PQ - Intergration testing

## Purpose

- receiving feedback from external hardware if the command given to the board was successfully executed
- verification
- when in space no-one can check if the led is actually on
- hard ware itself does not detect if the led is on itself
tests the intergration of the Delfi-PQ system

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


## How to use

### Hardware necessary
### Software

java file running - as local host
run python script

commend  to open and be in right directory 
libraries
py.serial library 


## Results

## Issues encountered

- the connection between board and egse is not established: remedy, try until it is


## Future changes and recommendations
instead of connecting to the led can be used 

