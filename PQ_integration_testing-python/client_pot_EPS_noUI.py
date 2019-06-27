#!/usr/bin/env python
'''
client_pot_ESP_noUI.py

Authors: Maxi Gallbrecht, Tiago Costa

This python script has the purpose to test the communication with the ESP
subsystem of the Delfi-PQ.

Here, the current of bus 3 within the housekeeping of the ESP is requested
while the digital potentiometer is set to deliver certain values to the EPS
in order to change the B3 current which is received through housekeeping.
With the use of the Arduino the digital potentiometer is controled.

'''

import threading
import sys
import pq_module as pq
import pq_comms as pqc
import time
import signal
import sys
import serial
#import logging

'''
FUNCTION signal_handler

    Input:sig, frame
    Output:None
    Purpose:To quit all threads, by turning the flag 'working' to False and
            exit the program.

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
    Purpose:To print a message in the terminal that gives the user the
            verification of communication with the board

'''
def process_frame(packet):
    print "\nCommand received in", packet['Source'], "\n"


'''
FUNCTION get_packets

    Input:None
    Output:None
    Purpose:To be used as a thread to communicate with the board after a command

'''
def get_packets():
    global working
    while working:
        pq_class.get_data()

'''
FUNCTION send_packets

    Input:None
    Output:None
    Purpose:To send a command to the board. It first sends a commands
            to the Arduino serial monitor to turn the digital potentiometer
            to LOW after which the housekeeping packet of the EPS is
            requested and the current value of Bus 3 is printed to the terminal.
            Then, the process is repeted only a command is sent to the Serial
            monitor to turn it High after which the program exits.

'''
def send_packets():
    global working

    print('\nThe pot will be turned LOW and then HIGH.')

    command = str.encode('1')
    arduino.write(command)         #send to Arduino
    print('Command to turn pot LOW sent to Arduino')

    time.sleep(1)

    sys.stdout.write('\nCommand received.\nSending to board->')
    pq_class.housekeeping("EPS")
    time.sleep(0.5)
    packets = pq_class.get_packets()
    time.sleep(1)
    if packets:
        for packet in packets:
            print(packet['Source'])
            if (packet['_received_'] == 'EPSHousekeepingReply'):
                print('\n Current of the EPS Bus 3: \n' )
                print(packet["B3_current"])
            process_frame(packet)

    time.sleep(3)

    command = str.encode('3')
    arduino.write(command)            #send to Arduino
    print('\nCommand to turn pot HIGH sent to Arduino')
    time.sleep(1)

    sys.stdout.write('\nCommand received.\nSending to board->')
    pq_class.housekeeping("EPS")
    time.sleep(0.5)
    packets = pq_class.get_packets()
    time.sleep(1)
    if packets:
        for packet in packets:
            print(packet['Source'])
            if (packet['_received_'] == 'EPSHousekeepingReply'):
                print('\n Current of the EPS Bus 3: \n' )
                print(packet["B3_current"])
            process_frame(packet)

    # future adaptation:
    # include verification if difference of both current values
    # is within an appropriate range

    time.sleep(3)

    print('\nProgramme done.')
    working=False
    time.sleep(2)
    print('Exit.')
    sys.exit()

'''
FUNCTION introduction

    Input:None
    Output:None
    Purpose:Initial message to the user after s/he runs the program
'''
def introduction():
    print("\n\n#################################################################")
    print("This application prints out the current value of Bus 3 of the EPS")
    print("It verifies the working state of the EPS with the use of a digital potentiometer and an Arduino")
    print("To exit the application press \'CTRL+C\'")
    print("#################################################################\n")

'''
FUNCTION choose_arduino_port

    Input:None
    Output:arduino
    Purpose:It asks the user to input the computer (or virtual box) port to
            which the Arduino is connected.
'''
def choose_arduino_port():

    port_number=input('Insert the arduino port (0,1,2,...):')
    arduino = serial.Serial(
    port='/dev/ttyACM'+str(port_number),\
    baudrate=9600)

    return arduino

'''
FUNCTION initialization

    Input:None
    Output:None
    Purpose:Verifies the connection with the board by pinging it 10 times. Only
            after 10 successful tries the main program continues. It pings once
            every second.
'''
def initialization():
    connected=False
    counter=1
    toolbar_width=10
    sys.stdout.write('Verifying connection with the board... sending 10 pings')
    sys.stdout.flush()

    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    while not connected:
        pq_class.ping_silent('ESP')
        packets = pq_class.get_packets()
        if packets:
            sys.stdout.write("#")
            sys.stdout.flush()
            counter += 1
        else:
            counter = 0 #If it failed one time, restarts to count

        if counter==10:
            print("\nConnected to the board!")
            #print("\nThe application is ready for the LED input (input 1 or 0 and press \'ENTER\')")
            connected=True

        try:
            time.sleep(0.3)
        except KeyboardInterrupt:  # Exits if the user presses CTRL+C while pinging
            working=False
            print("\nExit.")
            sys.exit()


TCP_IP = '127.0.0.1'
TCP_PORT = 10000
BUFFER_SIZE = 1024

working = True      # Flag that is used to end threads when the program is exiting
first_input=False   # Flag to only start to check after the first user input
wait_time=10        # Waiting time to recheck with Arduino

fname = sys.argv[1]

pq_class = pqc.pq(TCP_IP, TCP_PORT, 1, BUFFER_SIZE, fname, 10)

introduction()  # Initial user message

arduino=choose_arduino_port() # Choosing arduino port

t=threading.Thread(target=get_packets) # Comms with board
t.start()

initialization() # Verification of connection with the board

t2=threading.Thread(target=send_packets) # Sending commands
t2.start()

signal.signal(signal.SIGINT, signal_handler)  # Controls the exit of the program
