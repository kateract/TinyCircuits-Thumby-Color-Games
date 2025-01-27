#Scrolling clouds effect created by transistortester
#Inspired by the opening of the C64 demo "Uncensored" created by Booze Design: https://www.youtube.com/watch?v=9LFD4SzW3e0
#Press A to quit and B to toggle and outline

from engine_nodes import Sprite2DNode
from engine_resources import TextureResource
from engine_animation import Tween, ONE_SHOT, EASE_LINEAR
import engine
import engine_io
import engine_draw
import math
from time import ticks_ms, ticks_diff
from random import randint
from machine import freq

@micropython.viper
def fillscreen(fb, fill:int):
    scr = ptr16(fb)
    i:int = 0
    for i in range(16384):
        scr[i] = fill

cloudshape = bytearray([11, 11, 11, 12, 13, 14, 14, 14, 14, 14, 15, 15, 14, 12, 11, 10, 10, 9, 9, 9, 9, 10, 10, 11, 11, 11, 10, 10, 10, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 7, 8, 9, 12, 12, 13, 13, 14, 15, 16, 17, 19, 21, 22, 23, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 18, 16, 15, 15, 14, 14, 13, 13, 13, 13, 13, 14, 14, 15, 15, 14, 14, 14, 13, 13, 13, 13, 13, 11, 10, 9, 9, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9, 10, 11, 11, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 11, 11, 12, 13, 11, 10, 9, 8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 5, 6, 7, 7, 7, 7, 7, 7, 7, 8, 7, 5, 4, 4, 3, 3, 3, 3, 3, 4, 4, 5, 7, 9, 14, 15, 15, 15, 15, 16, 16, 16, 17, 17, 18, 18, 19, 20, 21, 21, 20, 19, 17, 16, 16, 15, 15, 15, 15, 15, 15, 15, 16, 16, 17, 15, 13, 12, 11, 11, 10, 10, 10, 10, 10, 11, 11])
cloudheight = max(cloudshape)
#engine.fps_limit(60)
#freq(150000000)

@micropython.viper
def drawcloud(fb, xoff:int, yoff:int, outline:int, shade:int, bgshade:int):
    xpos:int = 0
    ypos:int = 0
    bufpos:int = 0
    fill:int = 0
    cloudptr = ptr8(cloudshape)
    cloudsize:int = int(len(cloudshape))
    scr = ptr16(fb)
    while xpos < 128:
        bufpos = (yoff + cloudptr[(xpos+xoff)%cloudsize]) * 128 + xpos
        fill = outline
        if bufpos < 0:
            bufpos = xpos
            fill = shade
        while bufpos < 16384 and scr[bufpos] == bgshade: #small bug: if the previous cloud is *exactly* bgshade it will be overwritten
            scr[bufpos] = fill
            fill = shade
            bufpos += 128
        xpos += 1

def RGB888to565(c):
    return ((c[0]>>3)<<11) | ((c[1]>>2)<<5) | c[2]>>3

def buttonpress():
    if engine_io.A.is_just_pressed: return True
    if engine_io.B.is_just_pressed: return True
    if engine_io.UP.is_just_pressed: return True
    if engine_io.DOWN.is_just_pressed: return True
    if engine_io.LEFT.is_just_pressed: return True
    if engine_io.RIGHT.is_just_pressed: return True
    if engine_io.LB.is_just_pressed: return True
    if engine_io.RB.is_just_pressed: return True
    if engine_io.MENU.is_just_pressed: return True
    return False

class ScreenSaver(Sprite2DNode):
    def __init__(self):
        super().__init__(self)
        self.texture = TextureResource(128, 128)
        self.canvas = self.texture.data
        self.opacity = 0.0
        self.layer = 127
        self.tween = Tween()
        self.visible = False
        
        self.clouds = [] #each is [xpos, ypos, shade]
        self.nextcloud = 0
        self.fill = 0 #background colour
        self.lastpress = ticks_ms()
        self.timeout = 120 * 1000
    
    def update(self):
        self.nextcloud -= 1
        if self.nextcloud <= 0:
            t = ticks_ms()/7
            colour = RGB888to565([
                int(math.sin(math.radians(t*1.2+50)/5)*100+127),
                int(math.sin(math.radians(t+150)/5)*100+127),
                int(math.sin(math.radians(t*1.1)/5)*100+127)])
            self.clouds.append([randint(0, len(cloudshape)-1), 128.0, colour])
            self.nextcloud = 20
        if len(self.clouds) and self.clouds[0][1]+cloudheight < 0: #completely off screen
            self.fill = self.clouds.pop(0)[2] #remove layer, but set background colour just in case the next cloud isn't overlapping the top of the screen
        
        fillscreen(self.canvas, self.fill)
        
        t = ticks_ms()/2000
        for cloud in reversed(self.clouds):
            cloud[1] -= 0.5
            drawcloud(self.canvas, int(cloud[0] + math.sin(cloud[1]*0.07+t)*15), int(cloud[1]), int(cloud[2]), int(cloud[2]), self.fill)
    
    def tick(self, dt):
        if self.opacity > 0:
            self.update()
        if self.visible:
            if buttonpress():
                self.visible = False
                #self.opacity = 0
                self.tween.start(self, "opacity", None, 0.0, 200, 1.0, ONE_SHOT, EASE_LINEAR)
                self.lastpress = ticks_ms()
        else:
            if buttonpress():
                self.lastpress = ticks_ms()
            if ticks_diff(ticks_ms(), self.lastpress) > self.timeout:
                self.visible = True
                #self.opacity = 1
                self.tween.start(self, "opacity", None, 1.0, 1000, 1.0, ONE_SHOT, EASE_LINEAR)