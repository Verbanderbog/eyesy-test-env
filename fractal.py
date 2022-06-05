#!/usr/bin/env python
#Fractalss ver 0.1
#Vadim Kataev 2006
#www.compuvisor.net
#www.technopedia.org
#vkataev at gmail.com

#we use following fact:
# x ** ((0 + 1j) * t) = sinusoid movement
# x != 0,1

import sys, pygame, random, math, time
from pygame.locals import *

SCREEN_WIDTH=320; SCREEN_HEIGHT=200
CENTER_X=SCREEN_WIDTH/2; CENTER_Y=SCREEN_HEIGHT/2

max_iteration = 35
scale = 3.0/(SCREEN_HEIGHT*500.0)

def setup(screen,etc) :
	global SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_X, CENTER_Y, scale
	SCREEN_WIDTH = screen.get_width()
	SCREEN_HEIGHT = screen.get_height()
	CENTER_X = SCREEN_WIDTH / 2
	CENTER_Y = SCREEN_HEIGHT / 2
	scale = 3.0 / (SCREEN_HEIGHT * 1000.0)

def draw(screen, etc):
	etc.color_picker_bg(etc.knob5)
	draw_field(screen,etc)

def init():
	global screen, atoms, cell, font
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
	#font = pygame.font.Font('Vera.ttf', 9)
	#pygame.mouse.set_cursor((8,8), (0,0), (0,)*(64/8), (0,)*(64/8))	#Trick, no visible cursor

def cycle():
	return

def update_screen():
	global screen, mouse_pos
	screen.fill((255, 255, 255))
	draw_field(screen)
	pygame.display.flip()

def main():
	global scale
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
		cycle()
		update_screen()
		time.sleep(1000)

def iteration(c):
	i = 0
	z = 0
	mag = 0.0
	while mag<4.0 and i<max_iteration:
		z = z**2 + c
		mag = z.imag*z.imag + z.real*z.real
		i+=1
	return i

def set_color(i,etc):
	color = (0, 0, 0)
	if i == max_iteration:
		return color
	else:
		sel = etc.knob4 * 8
		Cmod = etc.knob3 * 2

		if 1 > sel:
			color = (int(127 + 127 * math.sin(i * 1 * Cmod + time.time())),
					 int(127 + 127 * math.sin(i * 1 * Cmod + time.time())),
					 int(127 + 127 * math.sin(i * 1 * Cmod + time.time())))
		if 1 <= sel < 2:
			color = (int(127 + 127 * math.sin(i * 1 * Cmod + time.time())), 0, 45)
		if 2 <= sel < 3:
			color = (255, int(155 + 100 * math.sin(i * 1 * Cmod + time.time())), 30)
		if 3 <= sel < 4:
			color = (0, 200, int(127 + 127 * math.sin(i * 1 * Cmod + time.time())))
		if 5 > sel >= 4:
			color = ((127 * Cmod) % 255,
					 (127 * Cmod) % 255,
					 int(127 + 127 * math.sin(i * (Cmod + .1) + time.time())))
		if 6 > sel >= 5:
			color = ((127 * Cmod) % 255,
					 int(127 + 127 * math.sin(i * (Cmod + .1) + time.time())),
					 (127 * Cmod) % 255)
		if 7 > sel >= 6:
			color = (int(127 + 127 * math.sin(i * (Cmod + .1) + time.time())),
					 (127 * Cmod) % 255,
					 (127 * Cmod) % 255)
		if sel >= 7:
			color = (int(127 + 127 * math.sin((i + 30) * (1 * Cmod + .01) + time.time())),
					 int(127 + 127 * math.sin((i + 30) * (.5 * Cmod + .005) + time.time())),
					 int(127 + 127 * math.sin((i + 15) * (.1 * Cmod + .001) + time.time())))
		return color

def draw_field(screen,etc):
	j = 0 + 1j
	for scr_x in range(int(SCREEN_WIDTH/2)):
		for scr_y in range(int(SCREEN_HEIGHT/2)):
			x = (scr_x - CENTER_X) * scale - 0.001
			y = (scr_y - CENTER_Y) * scale - 0.75
			c = x + y*j
			iter_value = iteration(c)
			if iter_value == max_iteration:
				continue
			col = set_color(iter_value,etc)
			pygame.draw.line(screen, col, (scr_x, scr_y), (scr_x, scr_y))
			pygame.draw.line(screen, col, (scr_x*-1+SCREEN_WIDTH-1, scr_y), (scr_x*-1+SCREEN_WIDTH-1, scr_y))
			pygame.draw.line(screen, col, (scr_x, scr_y*-1+SCREEN_HEIGHT-1), (scr_x, scr_y*-1+SCREEN_HEIGHT-1))
			pygame.draw.line(screen, col, (scr_x*-1+SCREEN_WIDTH-1, scr_y*-1+SCREEN_HEIGHT-1), (scr_x*-1+SCREEN_WIDTH-1, scr_y*-1+SCREEN_HEIGHT-1))
