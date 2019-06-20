#!/usr/bin/env python
'''
client_LED.py

Authors: Maxi Gallbrecht, Tiago Costa

This python script has the purpose to test the communication with a Texas
Launchpad that emulates the on-board software of the Delfi-PQ OBC.

Here, the LED of the Launchpad is tested and verified through communication with
the board itself and an Arduino, that reads the voltage levels

'''

import threading
import sys
import pq_module as pq
import pq_comms as pqc
import time
import signal
import serial
import logging

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
#    if packet['DBGSW1']=='ON':
#        print "Switch 1 is pressed"
#    if packet['DBGSW2']=='ON':
#        print "Switch 2 is pressed"

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
            flag is performed. Then, according to the user input, it either
            calls a function to turn ON or OFF the LED.

'''
def send_packets():
    global user
    global last_received
    global working
    while working:
        user_previous=user
        user_input(user_previous) # gets and verifies user input
        if not working:
            break      # If the program finished while the thread was in 'input'

        if user==0:
            sys.stdout.write('\nCommand received.\nSending to board->') # print with no '\n'
            pq_class.ledOFF()
            packets = pq_class.get_packets()
            time.sleep(0.5)  # to make sure everything changes appropriately
            if packets:
                for packet in packets:
                    process_frame(packet)

            check(0) # Immediatly check the arduino
        elif user==1:
            sys.stdout.write('\nCommand received.\nSending to board->')
            pq_class.ledON()
            packets = pq_class.get_packets()
            time.sleep(0.5)   # to make sure everything changes appropriately
            if packets:
                for packet in packets:
                    process_frame(packet)

            check(0) # Immediatly check the arduino

'''
FUNCTION user_input

    Input:user_previous
    Output:None
    Purpose:To interpret the user input in the terminal. If it's not 0 or 1, it
            uses the previous valid command. After the first input it changes
            the 'first_input' flag
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
            if user==0 or user==1:
                first_input=True
                break
            else:
                print("The command is incorrect. Try again.")
                user=user_previous

'''
FUNCTION receiving

    Input:arduino, connection
    Output:None
    Purpose:It checks the last line of the arduino serial monitor. It analyses
            the buffer and reads only the last line. If connection is False,
            it only checks once and leaves the function. Use True for threads.
'''
def receiving(arduino, connection):
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
        if connection==False: # When the connection to the arduino is being
            break             # established, check just one time

'''
FUNCTION check

    Input:wait_time
    Output:None
    Purpose:Checking with Arduino the feedback of the LED. In case the input and
            feedback differ, a log file is written ('log' function). If it is an
            immediate check after an input, the 'wait_time' variable is 0 and so
            it breaks the 'working' loop.
'''
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

'''
FUNCTION log

    Input:None
    Output:None
    Purpose:Writes in the log file the error that the 'check' function detected.
            It writes the date and details of the error.
'''
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

'''
FUNCTION introduction

    Input:None
    Output:None
    Purpose:Initial message to the user after s/he runs the program
'''
def introduction():
    print("\n\n#################################################################")
    print("Welcome to the LED verification software!")
    print("This application prints out every 10 seconds the Arduino feedback")
    print("The commands are: 1 to turn the LED ON, 0 to turn it OFF.")
    print("To exit the application press \'CTRL+C\'")
    print("#################################################################\n")

'''
FUNCTION choose_arduino_port

    Input:None
    Output:arduino
    Purpose:It asks for the user to input the computer (or virtual box) port to
            which the Arduino is connected. It avoids error with 'CTRL+C' input.
            It checks if there is feedback through a large number of iterations.
            Like that, it confirms that a valid connection can be established.
            It only breaks when a valid port is chosen.
'''
def choose_arduino_port():
    global last_received
    connected=False
    counter=0
    while not connected:
        flag=0
        try:
            port_number=input('Insert the arduino port (0,1,2,...):')
            arduino = serial.Serial(
                port='/dev/ttyACM'+str(port_number),\
                baudrate=9600)

            sys.stdout.write("Connecting")
            sys.stdout.flush()
            while not connected:
                receiving(arduino,connected)
                if last_received=='1' or last_received=='0':
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    counter+=1
                elif flag==1000000:  # Tries several times to receive data from the Arduino
                    print("\nWrong port. Try again")
                    break
                else:
                    flag+=1
                if counter==3:
                    print(" Connected to the Arduino!")
                    connected= True
        except KeyboardInterrupt: # if ctrl+c is pressed
            print('\nExit.')
            sys.exit() #quit
        except:
            print("Wrong port. Try again.")

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
        pq_class.ping_silent('DEBUG')
        packets = pq_class.get_packets()
        if packets:
            sys.stdout.write("#")
            sys.stdout.flush()
            counter += 1
        else:
            counter = 0 #If it failed one time, restarts to count

        if counter==10:
            print("\nConnected to the board!")
            print("\nThe application is ready for the LED input (input 1 or 0 and press \'ENTER\')")
            connected=True

        try:
            time.sleep(1)
        except KeyboardInterrupt:  # Exits if the user presses CTRL+C while pinging
            working=False
            print("\nExit.")
            sys.exit()


TCP_IP = '127.0.0.1'
TCP_PORT = 10000
BUFFER_SIZE = 1024

working = True      # Flag that is used to end threads when the program is exiting
first_input=False   # Flag to only start to check after the first user input
last_received = ''  # Arduino serial
user=0;             # User Input
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

t3=threading.Thread(target=receiving, args=(arduino,True,)) # Arduino serial monitor
t3.start()                                             # reading

t4=threading.Thread(target=check, args=(wait_time,))  # Arduino feedback
t4.start()

signal.signal(signal.SIGINT, signal_handler)  # Controls the exit of the program

while 1:
   pass  # Infinit loop
