import sys, pygame, random, math, time, numpy
from numpy import *
import numexpr as ne




def setup(screen,etc) :
	numpy.set_printoptions(threshold=numpy.inf)
	pass

def draw(screen, etc):
	etc.color_picker_bg(etc.knob5)
	n = screen.get_width()
	m = screen.get_height()
	itermax = 50
	xmin = -2
	xmax = 0.5
	ymin = -1.25
	ymax = 1.25
	print(mandel(screen ,etc, n, m, itermax, xmin, xmax, ymin, ymax))

def set_color(i,etc, itermax):
	color = (0, 0, 0)
	if i == itermax:
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

def mandel(screen ,etc, n, m, itermax, xmin, xmax, ymin, ymax):
	img = pygame.surfarray.array2d(screen)
	ix, iy = mgrid[0:n, 0:m]
	x = linspace(xmin, xmax, n)
	x.shape = n, 1
	y = linspace(ymin, ymax, m)
	y.shape = 1, m
	c = x + complex(0, 1) * y
	del x, y
	copyto(img, zeros(c.shape, dtype=numpy.int))
	ix.shape = n*m
	iy.shape = n*m
	c.shape = n*m
	z = copy(c)
	for i in range(itermax):
		if not len(z): break
		multiply(z, z, z)
		add(z, c, z)
		rem = abs(z)>2.0
		col = set_color(i+1, etc, itermax)
		#pygame.draw.line(screen, col, (int(ix[rem]), int(iy[rem])), (int(ix[rem]), int(iy[rem])))
		img[ix[rem], iy[rem]] = i+1
		rem = ~rem
		z = z[rem]
		ix, iy = ix[rem], iy[rem]
		c = c[rem]


	return img

def nemandel(screen ,etc, n, m, itermax, xmin, xmax, ymin, ymax,
			 depth=1):
	expr = 'z**2+c'
	for _ in range(depth-1):
		expr = '({expr})**2+c'.format(expr=expr)
	itermax = itermax/depth
	print ('Expression used:', expr)
	ix, iy = mgrid[0:n, 0:m]
	x = linspace(xmin, xmax, n)[ix]
	y = linspace(ymin, ymax, m)[iy]
	c = x+complex(0,1)*y
	del x, y # save a bit of memory, we only need z
	img = zeros(c.shape, dtype=int)
	ix.shape = n*m
	iy.shape = n*m
	c.shape = n*m
	z = copy(c)
	for i in range(itermax):
		if not len(z): break # all points have escaped
		z = ne.evaluate(expr)
		rem = abs(z)>2.0
		img[ix[rem], iy[rem]] = i+1
		rem = -rem
		z = z[rem]
		ix, iy = ix[rem], iy[rem]
		c = c[rem]
	img[img==0] = itermax+1
	return img