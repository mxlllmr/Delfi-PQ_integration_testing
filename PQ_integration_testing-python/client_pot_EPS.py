#!/usr/bin/env python
'''
client_pot_EPS.py

Authors: Maxi Gallbrecht, Tiago Costa

This python script has the purpose to test the communication with the EPS
subsystem of the Delfi-PQ.

Here, the current of bus 3 through the housekeeping command to the ESP is requested
while the digital potentiometer is set with the use of an Arduino (arduino_breakoutboard.ino)
to certain values in order to change the current value which is
received through housekeeping.
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
    print "Command received in", packet['Source'], "\n"


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
    Purpose:To send a command to the board. First, it calls the 'user_input'
            function, saving the previous input, in case the next one is
            not understood. As the input function stalls the thread, in case
            the program as finished, an extra verification of the 'working'
            flag is performed. Then, if the user input is 0, it
            calls a function to return the housekeeping packet from EPS
            and prints the current value of B3.

'''
def send_packets():
    global user
    global working
    while working:
        user_previous=user
        user_input(user_previous) # gets and verifies user input
        if not working:
            break      # If the program finished while the thread was in 'input'

        if user==0:
            sys.stdout.write('\nCommand received.\nSending to board->') # print with no '\n'
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

'''
FUNCTION user_input

    Input:user_previous
    Output:None
    Purpose:To interpret the user input in the terminal, if it is 0.
'''
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
            if user==0:
                first_input=True
                break
            else:
                print("The command is incorrect. Try again.")
                user=user_previous

'''
FUNCTION introduction

    Input:None
    Output:None
    Purpose:Initial message to the user after s/he runs the program
'''
def introduction():
    print("\n\n#################################################################")
    print("This application prints out the current value of Bus 3 of the EPS")
    print("Use this application together with arduino_breakoutboard.ino")
    print("The commands is: 0 to get the B3 current of the EPS through housekeeping.")
    print("To exit the application press \'CTRL+C\'")
    print("#################################################################\n")

'''
FUNCTION initialization

    Input:None
    Output:None
    Purpose:Verifies the connection with the board by pinging it 10 times. Only
            after 10 successful tries the main program continues. It pings once
            every 0.3 seconds.
'''
def initialization():
    global working
    connected=False
    counter=0
    toolbar_width=10
    sys.stdout.write('Verifying connection with the board... ')
    sys.stdout.flush()

    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    while not connected:
        pq_class.ping_silent('EPS')
        packets = pq_class.get_packets()
        if packets:
            sys.stdout.write("#")
            sys.stdout.flush()
            counter += 1
        else:
            counter = 0 #If it failed one time, restarts to count

        if counter==10:
            print("\nConnected to the board!")
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
user=0;             # User Input
wait_time=10        # Waiting time to recheck with Arduino

fname = sys.argv[1]

pq_class = pqc.pq(TCP_IP, TCP_PORT, 1, BUFFER_SIZE, fname, 10)

introduction()  # Initial user message

t=threading.Thread(target=get_packets) # Comms with board
t.start()

initialization() # Verification of connection with the board

t2=threading.Thread(target=send_packets) # Sending commands
t2.start()

signal.signal(signal.SIGINT, signal_handler)  # Controls the exit of the program

while 1:
   pass  # Infinit loop
