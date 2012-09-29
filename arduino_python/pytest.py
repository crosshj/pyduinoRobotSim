import struct
import serial
import binascii
import jserial
import sys
import time
from time import sleep



com_port = jserial.Select_Port()
t1=time.clock()
if com_port != "None":
	ser = jserial.init(com_port, 57600)
else:
	print ("No serial port available")
	sys.exit()
t2= time.clock()

try:
	while not ser.inWaiting():
		sleep(0)
	t3= time.clock()
	n=ser.read(3)
	if n == ">>>":
		print "Arduino is up."
	else:
		print "Not sure about Arduino status"
	t4=time.clock()
	n=ser.write("<<<".encode('ascii'))
	t5= time.clock()
except:
	print "UNABLE TO WRITE>>>"

try:
	while not ser.inWaiting():
		sleep(0.0)
	t6= time.clock()
	#text = ser.read(7).__repr__()
	n=ser.inWaiting()
	text = ser.read(n)
	t7= time.clock()
	print text
except:
	print "UNABLE TO READ>>>"

print "port setup time   - %0.3f" % ( (t2-t1) )
print "setup to 1st read - %0.3f" % ( (t3-t1) )
print "1st read          - %0.3f" % ( (t4-t3) )
print "write time        - %0.3f" % ( (t5-t4) )
print "write to 2nd read - %0.3f" % ( (t6-t5) )
print "2nd read          - %0.3f" % ( (t7-t6) )
ser.close()