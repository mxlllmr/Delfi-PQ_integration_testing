import json
import socket
import time
import signal

class pq:

    def __init__(self, ip, port, timeout, buffer_size, fname, log_period):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(timeout)
        self.s.connect((ip, port))
        self.buf = ""
        self.buffer_size = buffer_size
        self.data = ""

        self.f = open(fname,'a')
        self.log_period = log_period
        self.time_prev=  time.time()
        self.time_new =  0

    def close(self):
        self.f.close()
        self.s.close()

    def get_data(self):
        try:
            data = self.s.recv(self.buffer_size)
        except:
            return ""

        self.data += data

        self.f.write(data)
        #print "received data:", data
        self.time_new =  time.time()
        if self.time_new - self.time_prev > self.log_period*60:
            print 'Still here', self.time_new
            self.time_prev = self.time_new
            self.f.flush()

        return data

    def get_packets(self):

        packets = []
        sps = self.data.splitlines(True)
        self.data = ""
        for sp in sps:
            self.buf += sp
            if "\n" in self.buf:
                packet = json.loads(self.buf)
                self.buf = ""
                packets.append(packet)

        return packets

    def ping(self, destination):
        print "Sending"
        msg = {}
        msg['_send_'] = 'Ping'
        msg['Destination'] = destination

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")

    def housekeeping(self, destination):
        print "Sending"
        msg = {}
        msg['_send_'] = 'GetTelemetry' # Housekeeping command in the xml file
        msg['Destination'] = destination

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")

    def ledblink(self):
        msg = {}
        msg['_send_'] = 'DBGLEDcmd' # led debug command in the xml file
        msg['DBGLED'] = 'on'

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")

        msg = {}
        msg['_send_'] = 'DBGLEDcmd' # led debug command in the xml file
        msg['DBGLED'] = 'off'

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")

    def ledON(self):
        msg = {}
        msg['_send_'] = 'DBGLEDcmd' # led debug command in the xml file
        msg['DBGLED'] = 'on'

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")

    def ledOFF(self):
        msg = {}
        msg['_send_'] = 'DBGLEDcmd' # led debug command in the xml file
        msg['DBGLED'] = 'off'

        packet = json.dumps(msg, ensure_ascii=False)
        print packet
        self.s.send(packet + "\n")
