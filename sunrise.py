import os
import pygame
import random
import time
import math


def setup(screen,etc) :
    global star_points, audio_points, slow, last_peak
    star_points = [[0,0,time.time(),1,0,0]]
    audio_points = [[],[],[]]
    slow = 0
    last_peak = 0

def audio_peak(etc):
    a = etc.audio_in
    peak = 0
    for i in range(len(a)):
        if a[i] > peak:
            peak = a[i]
    return peak

def audio_transform(etc,n):
    a=etc.audio_in
    output = []
    for k in range(n):
        avg=0
        abs_avg=0
        for i in range(int(len(a)*k/n), int(len(a)*(k+1)/n)):
            avg += a[i]
            abs_avg += abs(a[i])
        avg = avg/(len(a)/n)
        abs_avg = abs_avg / (len(a) / n)
        variance = 0
        for i in range(int(len(a)*k/n), int(len(a)*(k+1)/n)):
           variance += (a[i]-avg) * (a[i]-avg)
        output.append([math.sqrt(variance),abs_avg])
    return output

def color_fade(start, end, c):
    return (start[0]-(start[0]-end[0])*c,start[1]-(start[1]-end[1])*c,start[2]-(start[2]-end[2])*c)

def plot_sun(etc, center_point, n, t, invert, inner_radius, middle_radius, outer_radius=None):
    points = []
    if outer_radius is None:
        outer_radius = middle_radius
    center_point = list(center_point)
    angle = 0
    if inner_radius>etc.xres*7/10:
        return points
    for i in range(n*2):
        if i % 2 == 0:
            r = outer_radius
        else:
            r = inner_radius
        if i % 4 == 0:
            r = middle_radius

        angle = i * (360/(2*n))+math.sin(t/2)*invert*5
        point=(math.cos(math.radians(angle)) * r + center_point[0], math.sin(math.radians(angle)) * r + center_point[1])
        if point[0]>etc.xres*1.25 or point[0]<etc.xres*-0.25 or point[1]>etc.yres*1.25 or point[1]<etc.yres*-0.25:
            continue
        points.append(point)
    return points

def color_sun(etc,i):
    color = etc.bg_color
    if i % 2 == 0:
        c = float(etc.knob4)
        norm_r = 240 * (c/0.15)
        norm_g = 248 * (c/0.15)
        norm_b = 110 * (c/0.15)
        color = (norm_r,norm_g,norm_b)
        if c > .15:
            r = math.sin(c * 2 * math.pi) * .5 + .5
            g = math.sin(c * 4 * math.pi) * .5 + .5
            b = math.sin(c * 8 * math.pi) * .5 + .5
            color = (r * 170+85, g * 170+85, b * 170+85)

        if c > .95:
            color = (int(127 + 127 * math.sin((30) * (1 + .01) + time.time())),
                     int(127 + 127 * math.sin((30) * (.5 + .005) + time.time())),
                     int(127 + 127 * math.sin((15) * (.1 + .001) + time.time())))
        if c >.99:
            color = (255, 255, 255)
    return color

def draw_suns(screen, etc):
    radius = etc.yres/(etc.knob3/2+1.25) - 10
    t=time.time()
    invert=1
    center_point = (etc.xres/2-(etc.knob1-0.5)*etc.xres*1.5, etc.yres*7/10-(etc.knob2-0.5)*etc.yres*2)
    skip=False
    for i in range(5):
        if i % 2 == 0:
            invert = -1*invert
        if radius<etc.xres*7/10 and not skip:
            sun=plot_sun(etc, center_point, 30, t, invert, radius-(audio_transform(etc,1)[0][1] * etc.yres/299999), radius+radius/12+(audio_peak(etc) * etc.yres/999999))
            if len(sun)>2:
                pygame.draw.polygon(screen,color_sun(etc,i),sun)
        else:
            skip = not skip
        radius -= etc.yres / 10
        if i % 2 == 1:
            radius -= etc.yres / 50

def plot_star(etc, center_point, n, t, invert, inner_radius, middle_radius, outer_radius=None):
    points = []
    if outer_radius is None:
        outer_radius = middle_radius
    center_point = list(center_point)
    angle = 0

    for i in range(n*2):
        if i % 2 == 0:
            r = outer_radius
        else:
            r = inner_radius
        if i % 4 == 0:
            r = middle_radius
        angle = i * (360/(2*n))+math.sin(t/2)*invert*5
        point=(math.cos(math.radians(angle)) * r + center_point[0], math.sin(math.radians(angle)) * r + center_point[1])
        points.append(point)
    return points


def peak_jump(etc):
    global last_peak
    ret_val = False
    curr_peak = audio_peak(etc)
    if curr_peak > last_peak*1.75:
         ret_val = True
    last_peak = curr_peak
    return ret_val


def draw_stars(screen, etc):
    while star_points[-1][0] < etc.xres*19/20:
        star_points.append([star_points[-1][0]+random.randrange(etc.xres/20,etc.xres/10),random.randrange(0,etc.yres*8/10),time.time(), 1 if random.random() < 0.5 else -1, False,0])

    if peak_jump(etc):
        star = random.randrange(0,len(star_points))
        max_loops = 10
        while star_points[star][4] and max_loops > 0:
            max_loops -= 1
            star = random.randrange(0, len(star_points))
        star_points[star][4] = True


    for i in range(len(star_points)):
        t=time.time()
        star_points[i][0] -= (t-star_points[i][2])*100
        star_points[i][2] = t
        if star_points[i][4]:
            star_points[i][5]+=0.2
            if star_points[i][5] >= 16:
                star_points[i][4]=False
        if not star_points[i][4]:
            star_points[i][5] = 0
        v = float(etc.knob2)
        color = etc.bg_color
        mod = star_points[i][5]
        if star_points[i][5] > 8:
            mod = 8-(star_points[i][5]-8)
        if v < 0.2:
            color = color_fade(color_sun(etc, 0),etc.bg_color,v/0.2)
        pygame.draw.polygon(screen,color,plot_star(etc,(star_points[i][0],star_points[i][1]),6,time.time(),star_points[i][3],3 + etc.knob3*3,3 + etc.knob3*12 + mod,3 + etc.knob3*9 + (mod*0.7)))

    while star_points[0][0] < 0:
        star_points.pop(0)

def color_hill(etc, reduce_brightness):
    c = float(etc.knob4)
    v = float(etc.knob2)
    norm_r = 240 * (c / 0.15)- reduce_brightness
    norm_g = 248 * (c / 0.15)- reduce_brightness
    norm_b = 110 * (c / 0.15)- reduce_brightness
    if norm_r < 0:
        norm_r = 0
    if norm_g < 0:
        norm_g = 0
    if norm_b < 0:
        norm_b = 0
    color = (norm_r, norm_g, norm_b)
    if c > .15:
        r = math.sin(c * 2 * math.pi) * .5 + .5
        g = math.sin(c * 4 * math.pi) * .5 + .5
        b = math.sin(c * 8 * math.pi) * .5 + .5
        color = (r * 150 + 105 - reduce_brightness, g * 150 + 105 - reduce_brightness, b * 150 + 105 - reduce_brightness)
    if c > 0.95:
        color = (int(185 + 70 * math.sin((30) * (1 + .01) + time.time()))- reduce_brightness,
                 int(185 + 70 * math.sin((30) * (.5  + .005) + time.time()))- reduce_brightness,
                 int(185 + 70 * math.sin((15) * (.1  + .001) + time.time()))- reduce_brightness)
    if c > .99:
        color = (255- reduce_brightness, 255- reduce_brightness, 255- reduce_brightness)
    if v<0.5:
        color = list(color)
        for i in range(3):
            color[i]=color[i]-(0.5-v)*190
            if color[i]<0:
                color[i]=0
        color=tuple(color)

    return color

def draw_hill(screen, etc, hill, color, height, offset, period, amplitude):
    global audio_points, slow

    divisions=50

    line_length = etc.xres/divisions
    if period == 0:
        period = 1
    while len(audio_points[hill]) < divisions+1:
        audio_points[hill].append([period, amplitude])
    audio_points[hill].append([period, amplitude])
    #if len(audio_points[hill]) > 2:
        #slower = 2 if float(etc.knob2) < 0.2 or float(etc.knob2) > 0.85 or float(etc.knob1) > 0.85 or float(etc.knob1) < 0.25 else 0
        #if slow < 2+slower:
            #pygame.draw.polygon(screen, color, audio_points[hill])
            #return
        #for i in range(2, len(audio_points[hill]) - 1):
            #audio_points[hill][i]=(audio_points[hill][i][0], audio_points[hill][i + 1][1])
        #audio_points[hill].pop()
    audio_points[hill].pop()

    points = [(etc.xres, etc.yres), (0, etc.yres)]
    #(etc.audio_in[int(i*100/((etc.xres/line_length)+1))] / 30000)+
    #while audio_points[hill][-1][0] < etc.xres:
        #audio_points[hill].append(((len(audio_points[hill]) - 2) * line_length, (math.sin((time.time() * 5 + offset + ((len(audio_points[hill]) - 2) * line_length) / (etc.xres / period)) / 2) * amplitude + height)))
    for i in range(divisions+1):
        points.append((i*line_length, math.sin(time.time()+offset+(i*line_length)/(etc.xres/audio_points[hill][i][0]))*audio_points[hill][i][1]+height+etc.audio_in[int((i/(divisions+1))*100)]/999))
    pygame.draw.polygon(screen, color, points)


def draw_hills(screen, etc):
    global slow
    #slow += 1
    #slower = 2 if float(etc.knob2) < 0.2 or float(etc.knob2) > 0.85 or float(etc.knob1) > 0.85 or float(etc.knob1) < 0.25 else 0
    #if slow >= 3+slower:
        #slow = 0
    transform = audio_transform(etc,3)
    draw_hill(screen, etc,0, color_hill(etc,0), etc.yres - etc.yres * 3 / 10, 0, (transform[0][0]+1)*20/399999, 50+transform[0][1]/9999)
    draw_hill(screen, etc,1, color_hill(etc,30), etc.yres - etc.yres * 2 / 10, math.pi, (transform[1][0]+1)*15/399999, 45+transform[1][1]/9999)
    draw_hill(screen, etc,2, color_hill(etc,60), etc.yres - etc.yres * 1 / 10, math.pi/2, (transform[2][0]+1)*11/399999, 35+transform[2][1]/9999)

def draw_aurora(screen, etc):
    pass

def draw_auroras(screen, etc):
    pass


def draw(screen, etc):
    etc.color_picker_bg(etc.knob5)
    v = float(etc.knob2)
    if v<0.5:
        color = list(etc.bg_color)
        for i in range(3):
            color[i]=color[i]-(0.5-v)*100
            if color[i]<0:
                color[i]=0
        etc.bg_color=tuple(color)
    draw_stars(screen, etc)
    draw_suns(screen, etc)
    draw_auroras(screen, etc)
    draw_hills(screen, etc)