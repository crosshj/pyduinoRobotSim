import pygame
import os,sys
from struct import *
from pygame.locals import *
import time
from time import sleep

import jserial
from jserial import *
from jpygame import *

SPEED = 1

(screen, bg, bg_lum, robot, robot_center_x, robot_center_y, robot_x, robot_y, bg_start) = init_board()

# Speed in pixels per frame
x_speed=0
y_speed=0

""" COM PORT INIT """
com_port = Select_Port()
if com_port != "None":
	ser = init_com(com_port, 57600)
	if do_handshake(ser):
		app_title = 'Robot Sim - Serial Mode [' + com_port + "]"
		arduino_connected = 1;
	else:
		app_title = 'Robot Sim - Keyboard Mode'
		arduino_connected = 0;
else:
	sleep(2)
	arduino_connected = 0;
	app_title = 'Robot Sim - Keyboard Mode'

set_title_text(screen,app_title) 




clock = pygame.time.Clock()
done=False
prevVal = None

while done==False:
	if arduino_connected:
		if ser.inWaiting() >= 5:
			serialValue = ser.read(5)
		
			if (serialValue == "_LINE"):
				do_line_sense(ser, screen, bg_lum,robot_center_x,robot_center_y)
			elif (serialValue == "_MOTO"):
				(x_speed, y_speed) = do_motors(ser, x_speed, y_speed)
			elif (serialValue == "_TASK"):
				do_task(ser)
			elif not serialValue == '':
				print "OTHER DATA --- {}".format(serialValue.__repr__())				
		
	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			done=True
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x_speed=-1*SPEED
			if event.key == pygame.K_RIGHT:
				x_speed=1*SPEED
			if event.key == pygame.K_UP:
				y_speed=-1*SPEED
			if event.key == pygame.K_DOWN:
				y_speed=1*SPEED

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				x_speed=0
			if event.key == pygame.K_RIGHT:
				x_speed=0
			if event.key == pygame.K_UP:
				y_speed=0
			if event.key == pygame.K_DOWN:
				y_speed=0
			if event.key == pygame.K_ESCAPE:
				done = True
				
	screen.blit( bg, bg_start )
	robot_x=robot_x+x_speed
	robot_y=robot_y+y_speed
	robot_center_x += x_speed
	robot_center_y += y_speed
	screen.blit( robot, [robot_x,robot_y])
	pygame.display.update()
	# Move the object according to the speed vector.
	clock.tick(120)




pygame.mouse.set_visible(True)
pygame.quit ()
