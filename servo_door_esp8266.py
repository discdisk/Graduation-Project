import time
import socket
from machine import Pin
import machine
trig = Pin(5, Pin.OUT)    # create output pin on GPIO0
echo = Pin(4, Pin.IN)     # create input pin on GPIO2
space1 = Pin(2, Pin.IN) 
space2 = Pin(14, Pin.IN) 
servo = machine.PWM(machine.Pin(0), freq=50)
servo.duty(30)

def checkdist():
    distance=[0,0,0,0,0,0,0,0,0,0]

    for i in range(10):
        trig.high()               # set pin to high
        time.sleep_us(15)
        trig.low()                # set pin to low
        start = time.ticks_ms() # get millisecond counter
        while not echo.value():
            delta = time.ticks_diff(time.ticks_ms(), start)
            if delta>100:
                trig.high()               # set pin to high
                time.sleep_us(15)
                trig.low() 
        start = time.ticks_us() # get millisecond counter
        while echo.value():
            pass
        delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
        distance[i]=delta/10000*170
    return (sum(distance)/10)

import network

wlan = network.WLAN(network.STA_IF) 
wlan.active(False)
ap = network.WLAN(network.AP_IF) 
ap.active(True)
ap.config(essid='ESP-AP')
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        print(line)
        line_decode=line.decode()
        splited=line_decode.split(' ')
        if len(splited)>1:
            if splited[0]=='GET':
                print(splited)
                request=splited[1].split('/')[1]
                print(request)
                cl.send("""HTTP/1.0 200 OK\r\nServer: NodeMCU on ESP8266\r\nContent-Type: text/html\r\n\r\n""")
                if request=='check':
                    cl.send(str(checkdist()))
                elif request=='complete':
                    servo.duty(100)
                    time.sleep(2)
                    servo.duty(30)
                    cl.send('complete')
                elif request=='space':
                    if space1.value()==0:
                        cl.send('space1 is taken     ')
                    else:
                        cl.send('space1 is empty     ')
                    if space2.value()==0:
                        cl.send('space2 is taken')
                    else:
                        cl.send('space1 is empty')
        if not line or line == b'\r\n':
            break
    cl.close()
