import serial
from xbee import XBee
import re
import requests
import time

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(serial_port)
while True:
    try:
        print xbee.wait_read_frame()['rf_data']
        
    except KeyboardInterrupt:
        
        break

serial_port.close()
