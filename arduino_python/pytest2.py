#import serial
#import binascii
import jserial
import sys
import time
from time import sleep

def do_handshake():
	ser.write(1)
	try:
		while not ser.inWaiting():
			sleep(0)
		n=ser.read(3)
		if n == ">>>":
			print "Arduino is up."
			handshake1 = 1
		else:
			print "Not sure about Arduino status"
			handshake1 = 0
		n=ser.write("<<<".encode('ascii'))
		while not ser.inWaiting():
			sleep(0.0)
		n=ser.read(3)
		if n == "<<<":
			print "Handshake complete."
			handshake2 = 1
		else:
			print "Handshake unshure."
			handshake2 = 0
	except:
		print "Serial port unavailable."
		handshake1 = handshake2 = 0
		
	return (handshake1 * handshake2)

com_port = jserial.Select_Port()
if com_port != "None":
	ser = jserial.init(com_port, 57600)
else:
	print ("No serial port available")
	sys.exit()

print do_handshake()


ser.close()