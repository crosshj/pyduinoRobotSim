import pygame
from pygame.locals import *
import numpy as np
import serial
from time import sleep
import sys
import random
import os

FULLSCREEN = 0

def init_board():
	pygame.init()
	if not pygame.font: print 'Warning, fonts disabled'
	if not pygame.mixer: print 'Warning, sound disabled'

	bg=pygame.image.load( './simulator/course.png' )
	bg_lum=pygame.image.load( './simulator/course_lum.png' )
	if FULLSCREEN:
		screen = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN )
	else:
		os.environ['SDL_VIDEO_WINDOW_POS'] = '20,40'
		screen = pygame.display.set_mode( (900, 720))
	bg = bg.convert()
	bg_lum = bg_lum.convert_alpha()
	robot = pygame.image.load( './simulator/robot.png' ).convert_alpha()
	pygame.mouse.set_visible(False)
	bg_start  = ( (screen.get_size()[0] - bg.get_size()[0])/2 ,(screen.get_size()[1] - bg.get_size()[1])/2)
	# robot's starting position
	robot_x=bg_start[0]+bg.get_size()[0] - 99
	robot_y=bg_start[1]+bg.get_size()[1] - 193
	robot_center_x =  round(robot.get_size()[0]/2) -1 + robot_x
	robot_center_y =  round(robot.get_size()[1]/2) +0 + robot_y

	screen.blit( bg_lum, bg_start )
	screen.blit( bg, bg_start )
	screen.blit( robot, [robot_x,robot_y])

	pygame.display.update()

	set_title_text(screen, "Waiting for Arduino to connect....")

	print "DISPLAY             [OKAY]"
	return (screen, bg, bg_lum, robot, robot_center_x, robot_center_y, robot_x, robot_y, bg_start)

def set_title_text(screen, text):
	# display Arduino waiting text
	if pygame.font:
		# erase old text
		screen.blit(pygame.Surface((screen.get_size()[0],45)),(0,0))
		pygame.display.update()
		font = pygame.font.Font(None, 36)
		text = font.render(text, True, (200,200, 200), (0,0,0))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = 30
		screen.blit(text, textpos)
		pygame.display.update()

# not working just now
def init(app_title):
	if not pygame.font: print 'Warning, fonts disabled'
	if not pygame.mixer: print 'Warning, sound disabled'

	pygame.init()
	SPEED = 2


	bg=pygame.image.load( './simulator/course.png' )
	screen = pygame.display.set_mode( (0, 0) ,pygame.FULLSCREEN  )
	bg = bg.convert()
	robot = pygame.image.load( './simulator/robot.png' ).convert_alpha()
	pygame.mouse.set_visible(False)

	bg_start  = ( (screen.get_size()[0] - bg.get_size()[0])/2 ,(screen.get_size()[1] - bg.get_size()[1])/2)
	#bg_start_y = screen.get_size()[1] - bg.get_size()[1]


	screen.blit( bg, bg_start )

	#time.sleep(3)

	#image_file = "course.gif"
	#img = Image.open(image_file)
	#width, height = img.size




	# Speed in pixels per frame
	x_speed=0
	y_speed=0
	# Current position
	x_coord=screen.get_size()[0] - 350
	y_coord=screen.get_size()[1] - 255

	# This sets the name of the window
	#pygame.display.set_caption('CMSC 150 is cool')


	#screen = pygame.display.set_mode((width, height))
	# Create a surface we can draw on
	#background_image = pygame.image.load("course.gif").convert()

	#background = pygame.Surface(screen.get_size())


	clock = pygame.time.Clock()

	if pygame.font:
			# Create a font
			font = pygame.font.Font(None, 36)

			# Render the text
			text = font.render(app_title, True, (200,200, 200), (0,0,0))

			# Create a rectangle
			textpos = text.get_rect()

			# Center the rectangle
			textpos.centerx = screen.get_rect().centerx
			textpos.centery = (screen.get_size()[1] - bg.get_size()[1])/4
			#textpos.centery = bg.get_rect().centery

			# Blit the text
			screen.blit(text, textpos)

	#this = String.draw_string_with_bg ("This is Times", "Times", 16, 1, (0, 0, 0),(200, 200, 200))
	#bg.blit (this, (5, 5))


# Function to draw the background
def draw_background(screen):
	# Set the screen background
	screen.fill(black)


def draw_item(screen,x,y):
	screen.blit( robot, [x,y])
	#pygame.draw.rect(screen,green,[0+x,0+y,40,55],0)
	#pygame.draw.circle(screen,black,[15+x,5+y],7,0)


def get_all_sensors(screen, surface, robot_center_x, robot_center_y):
	x_spread = 5
	y_spread = 5

	sensor_offset = [

	                [-2*x_spread, -2*y_spread],
	                [-1*x_spread, -2*y_spread],
	                [ 0*x_spread, -2*y_spread],
	                [ 1*x_spread, -2*y_spread],

	                [ 2*x_spread, -2*y_spread],
	                [ 2*x_spread, -1*y_spread],
	                [ 2*x_spread,  0*y_spread],
	                [ 2*x_spread,  1*y_spread],

	                [ 2*x_spread,  2*y_spread],
	                [ 1*x_spread,  2*y_spread],
	                [ 0*x_spread,  2*y_spread],
	                [-1*x_spread,  2*y_spread],

	                [-2*x_spread,  2*y_spread],
	                [-2*x_spread,  1*y_spread],
	                [-2*x_spread,  0*y_spread],
	                [-2*x_spread, -1*y_spread]

	                ]

	sensor_data = [0]*16
	#print sensor_offset
	alpha_map=pygame.surfarray.array_alpha(surface)
	np.array(sensor_data,dtype=np.uint8)
	surface_start  = ( (screen.get_size()[0] - surface.get_size()[0])/2 ,(screen.get_size()[1] - surface.get_size()[1])/2)
	for i in range(len(sensor_data)):
		 sensor_data[i] = int(alpha_map[sensor_offset[i][0]+robot_center_x-surface_start[0],
		 									 sensor_offset[i][1]+robot_center_y-surface_start[1]])
	return (sensor_data)

def do_line_sense(ser, screen, bg_lum,robot_center_x,robot_center_y):
	sensor_data = get_all_sensors(screen, bg_lum,robot_center_x,robot_center_y)
	#print "Sensor data: %s" % sensor_data

	for i in sensor_data:
		ser.write(chr(i))

	while ser.inWaiting() < 16:
		sleep(1)

	sensors_got = ser.read(16)
	sensors_got = [ord(c) for c in sensors_got]
	#print "Sensors got: %s" % sensors_got
	if sensor_data == sensors_got:
		ser.write("_LINE".encode('ascii'))
		print "LINE SENSORS CALL [OKAY] - {}".format(sensor_data)


def do_motors(ser, x_speed, y_speed):

	ser.write("_OKAY".encode('ascii'))

	while ser.inWaiting() < 4:
		sleep(0)

	motors_got = ser.read(4)
	motors_got = [( (ord(c)-127)*2)-1 for c in motors_got]
	#print "MOTORS CALL         [OKAY] - {}".format(motors_got)

	ser.write("_MOTO".encode('ascii'))

	if ( motors_got[0] > 0 and motors_got[1] > 0 and motors_got[2] > 0 and motors_got[3] > 0):
		x_speed = -1*motors_got[0]/255
		y_speed = 0
	if ( motors_got[0] < 0 and motors_got[1] < 0 and motors_got[2] < 0 and motors_got[3] < 0):
		x_speed = -1*motors_got[0]/255
		y_speed = 0
	if ( motors_got[0] > 0 and motors_got[1] < 0 and motors_got[2] < 0 and motors_got[3] > 0):
		x_speed = 0
		y_speed = motors_got[0]/255
	if ( motors_got[0] < 0 and motors_got[1] > 0 and motors_got[2] > 0 and motors_got[3] < 0):
		x_speed = 0
		y_speed = motors_got[0]/255
	if ( motors_got[0] == 0 and motors_got[1] == 0 and motors_got[2] == 0 and motors_got[3] == 0):
		x_speed = 0
		y_speed = 0



	return (x_speed, y_speed)

def do_task(ser):
	random.seed()

	task_data =  [ random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1) ]
	for i in task_data:
		ser.write(chr(i))

	while ser.inWaiting() < 4:
		sleep(1)

	task_got = ser.read(4)
	task_got = [ord(c) for c in task_got]
	task_data[0] = task_got[0]
	if task_data == task_got:
		ser.write("_TASK".encode('ascii'))
		print "TASK SENSORS CALL [OKAY] - {}".format(task_got)
	else:
		print "TASK SENSORS CALL [FAIL] - {} \n       {}".format( task_data, task_got )
