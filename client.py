#!/usr/bin/env python

import threading
import sys
import pq_module as pq
import pq_comms as pqc
import time
import signal
import sys
import serial
import logging

'''
FUNCTION signal_handler

    Input:sig, frame
    Output:None
    Purpose:...

'''
def signal_handler(sig, frame):
    global working
    working = False
    print('\nYou pressed Ctrl+C!  Press \'ENTER\' to exit, and wait for the program to finish.')
    pq_class.close()
    sys.exit(0)


'''
FUNCTION process_frame

    Input:packet
    Output:None
    Purpose:...

'''
def process_frame(packet):
    print "Command received in", packet['Source'], "\n"
#    if packet['DBGSW1']=='ON':
#        print "Switch 1 is pressed"
#    if packet['DBGSW2']=='ON':
#        print "Switch 2 is pressed"

def get_packets():
    global working
    while working:
        pq_class.get_data()

def send_packets():
    global user
    global last_received
    global working
    global first_input
    while working:
        user_previous=user
        user_input(user_previous) # gets and verifies user input
        if not working:
            break

        if user==0:
            sys.stdout.write('\nCommand received.\nSending to board->') # print with no '\n'
            pq_class.ledOFF()
            packets = pq_class.get_packets()
            time.sleep(1)
            if packets:
                for packet in packets:
                    process_frame(packet)

            check(0) # Immediatly check the arduino
        elif user==1:
            sys.stdout.write('\nCommand received.\nSending to board->')
            pq_class.ledON()
            packets = pq_class.get_packets()
            time.sleep(1)
            if packets:
                for packet in packets:
                    process_frame(packet)

            check(0) # Immediatly check the arduino

def user_input(user_previous):
    global user
    global working
    global first_input

    while 1:
        try:
            user=input()
        except:
            if working==False:
                break
            else:
                print("The command is incorrect. Try again.")
                user=user_previous
        else:
            if user==0 or user==1:
                first_input=True
                break
            else:
                print("The command is incorrect. Try again.")
                user=user_previous

def receiving(arduino):
    global last_received
    global working

    buffer_string = ''
    while working:
        buffer_string = buffer_string + arduino.read(arduino.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]

def check(wait_time):
    global user
    global last_received
    global working
    global first_input

    while working:  # Wait time has to be !=0 for recheck and =0 for immediate check
        if first_input==True:
            if user==1 and last_received=='1':
                print("Arduino: The LED is ON.")
            elif user==0 and last_received=='0':
                print("Arduino: The LED is OFF.")
            elif user==0 and last_received=='1':
                print("\nERROR: The LED is ON, despite the input. Logfile generated")
                log()
                print("Input set to 1\n")
                user=1
            elif user==1 and last_received=='0':
                print("\nERROR: The LED is OFF, despite the input. Logfile generated")
                log()
                print("Input set to 0\n")
                user=0

        if wait_time==0:
            break

        time.sleep(wait_time)

def log():
    global user
    global last_received
    if last_received=='0':
        led='OFF'
    else:
        led='ON'

    logging.basicConfig(filename='log_LED.log', pathname='./log_LED.log',
    format='%(asctime)s - %(levelname)s - %(message)s\n',
                        datefmt='%d-%b-%y %H:%M:%S')
    logging.error('Input was '+str(user)+' and LED was '+led+
    '\nArduino detected an unwanted output. Check connections and boards')

def introduction():
    print("\n\n#################################################################")
    print("Welcome to the LED detection software!")
    print("This application prints out every 10 seconds the Arduino feedback")
    print("The commands are: 1 to turn the LED ON, 0 to turn it OFF.")
    print("To exit the application press \'CTRL+C\'")
    print("#################################################################\n")


def choose_arduino_port():
    while 1:
        try:
            port_number=input('Insert the arduino port (0,1,2,...):')
            arduino = serial.Serial(
                port='/dev/ttyACM'+str(port_number),\
                baudrate=9600)
        except KeyboardInterrupt: # if ctrl+c is pressed
            print('\nExit.')
            sys.exit() #quit
        except:
            print("Wrong port. Try again.")
        else:
            break
    print("The application is ready for the LED input (input 1 or 0 and press \'ENTER\')")

    return arduino


TCP_IP = '127.0.0.1'
TCP_PORT = 10000
BUFFER_SIZE = 1024

working = True
first_input=False   # Flag to only start to check after the first user input
last_received = ''  # Arduino serial
user=0;             # USer Input
wait_time=10        # Waiting time to recheck with Arduino

fname = sys.argv[1]

pq_class = pqc.pq(TCP_IP, TCP_PORT, 1, BUFFER_SIZE, fname, 10)

introduction()

arduino=choose_arduino_port()

t=threading.Thread(target=get_packets)
t.start()

t2=threading.Thread(target=send_packets)
t2.start()

t3=threading.Thread(target=receiving, args=(arduino,))
t3.start()

t4=threading.Thread(target=check, args=(wait_time,))
t4.start()

signal.signal(signal.SIGINT, signal_handler)

while 1:
   pass
