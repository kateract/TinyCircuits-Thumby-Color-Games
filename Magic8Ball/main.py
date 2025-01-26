import engine_main
import engine
import engine_io
import engine_save
from engine_resources import TextureResource, FontResource
from engine_nodes import Sprite2DNode, Rectangle2DNode, CameraNode, Text2DNode, EmptyNode
from engine_animation import Tween, ONE_SHOT, EASE_LINEAR, EASE_SINE_OUT, EASE_QUAD_OUT, EASE_CUBIC_OUT, EASE_QUART_OUT, EASE_QUINT_OUT, EASE_EXP_OUT, EASE_CIRC_OUT, EASE_BACK_OUT
from engine_math import Vector2, Vector3
from engine_draw import Color
import random
import gc
from micropython import mem_info
from math import radians, sin
from time import ticks_ms, ticks_diff


def printmem(reason=None, heap=False, collect=True):
    if collect: gc.collect()
    freemem = gc.mem_free()
    totalmem = gc.mem_alloc() + freemem
    print("\n" + "="*79)
    if reason: print(f"***{reason}***")
    print(f"{(totalmem-freemem)/totalmem*100}% RAM used")
    if heap: mem_info(1)
    else: mem_info()
    print("="*79)


easeout = [EASE_SINE_OUT, EASE_QUAD_OUT, EASE_CUBIC_OUT, EASE_QUART_OUT, EASE_QUINT_OUT, EASE_EXP_OUT, EASE_CIRC_OUT] #normal easings

triangletex = TextureResource("/Games/Magic8Ball/triangle.bmp", True)
gradienttex = TextureResource("/Games/Magic8Ball/gradient.bmp", True)
#font = FontResource("/Games/Magic8Ball/Portfolio6x8-4bit.bmp", True)
font = FontResource("/Games/Magic8Ball/Portfolio6x8-1bit.bmp", True)

textcolor = Color(0.7,0.7,1)
textcolor_selected = Color(0.3,0.3,1)
menucolor = Color(0.0,0.0,0.1)

camera = CameraNode()

engine_save.set_location("settings")

#rumblesetting = 4
rumblesetting = engine_save.load("rumble", 4)
rumbledata = [[f"{i*10}%", i/10.0] for i in range(10+1)]
rumbledata[0][0] = "Off"
rumbledata[4][0] = "40% (default)"
vibstrength = rumbledata[rumblesetting][1]

#raritysetting = 3
raritysetting = engine_save.load("rarity", 3)
raritydata = [["Off", None], ["Very rare", 100], ["Rare", 50], ["Uncommon (default)", 20], ["Occasional", 10], ["Common", 5], ["Very common", 2]] #will appear 1 in n responses on average
rarity = raritydata[raritysetting][1]


class TextContainer(EmptyNode):
    def __init__(self):
        super().__init__(self)
        self.text = [] #if no reference is kept, child nodes will eventually be garbage collected


class Magic8(Sprite2DNode):
    def __init__(self):
        super().__init__(self)
        self.texture = triangletex
        self.layer = 0
        
        self.gradient = Sprite2DNode(texture=gradienttex, layer=2)
        self.gradcontainer = EmptyNode() #absolute rotation/position is applied to this, to allow self.gradient to be transformed relative to rotation
        self.gradcontainer.add_child(self.gradient)
        self.gradcontainer.rotation = 0
        self.textcontainer = None
        
        self.tween_rot = Tween()
        self.tween_opacity = Tween()
        self.tween_pos_x = Tween()
        self.tween_pos_y = Tween()
        self.tween_scale = Tween()
        self.tween_grad_rot = Tween()
        self.tween_grad_scale = Tween()
        
        self.disappeartime = None
    
    def settext(self, text, rotated=False, scale=1, offset=0):
        self.mark_destroy_children()
        
        self.textcontainer = TextContainer()
        fontheight = 8*scale
        
        lines = text.splitlines()
        ypos = offset - (len(lines)*fontheight/2 - fontheight/2)
        
        if rotated:
            self.textcontainer.rotation = radians(60)
        
        for i in lines:
            node = Text2DNode(font=font, text=i.strip(), layer=1, scale=Vector2(scale,scale), position=Vector2(0,ypos), color=textcolor)
            self.textcontainer.add_child(node)
            self.textcontainer.text.append(node)
            ypos += fontheight
        
        self.add_child(self.textcontainer)
    
    def appear(self, text=None):
        if text == None:
            if rarity == None or random.randint(1, rarity) != 1:
                text = random.choice(responses)
            else:
                text = random.choice(responses_rare)
        self.settext(*text)
        
        rot_target = radians(random.randint(-40, 40))
        if text[1]: rot_target -= radians(60)
        self.rotation = rot_target + radians(random.randint(-20, 20))
        self.tween_rot.start(self, "rotation", None, rot_target, random.randint(1000,3000), 1.0, ONE_SHOT, random.choice(easeout))
        
        self.opacity = 0.0
        appeartime = random.randint(1000,2000)
        self.tween_opacity.start(self, "opacity", None, 1.0, appeartime, 1.0, ONE_SHOT, EASE_SINE_OUT)
        #self.scale = Vector2(0.9,0.9)
        #self.tween_scale.start(self, "scale", None, Vector2(1.0,1.0), appeartime, 1.0, ONE_SHOT, EASE_SINE_OUT)
        
        self.position = Vector2(random.randint(-10,10), random.randint(-10,10))
        self.tween_pos_x.start(self.position, "x", None, float(self.position.x+random.randint(-5,5)), random.randint(2000,4000), 1.0, ONE_SHOT, random.choice(easeout))
        self.tween_pos_y.start(self.position, "y", None, float(self.position.y+random.randint(-5,5)), random.randint(2000,4000), 1.0, ONE_SHOT, random.choice(easeout))
        
        gradrot_target = radians(random.randint(0, 360))
        self.gradcontainer.rotation = gradrot_target + radians(random.randint(-360, 360))
        self.tween_grad_rot.start(self.gradcontainer, "rotation", None, gradrot_target, random.randint(2000,3500), 1.0, ONE_SHOT, EASE_BACK_OUT)
        
        self.gradient.scale = Vector2(1.0,0.8)
        self.tween_grad_scale.start(self.gradient, "scale", None, Vector2(1.0,1.0+random.random()/2), random.randint(1000,3000), 1.0, ONE_SHOT, random.choice(easeout))
    
    def shake(self):
        self.tween_opacity.start(self, "opacity", None, 0.0, random.randint(100,300), 1.0, ONE_SHOT, EASE_SINE_OUT)
        self.disappeartime = ticks_ms()
    
    def tick(self, dt):
        self.gradcontainer.position = self.position
        if self.disappeartime != None:
            ticks = ticks_diff(ticks_ms(), self.disappeartime)
            if ticks > 200:
                engine_io.rumble(max(0.0, sin(radians(ticks*2) + sin(radians(ticks/6+200))*3)*vibstrength)) #FM waveform for a little more complexity. Parameters were chosen somewhat arbitrarily by feel.
            else:
                engine_io.rumble(0.0)
            if ticks > 2000:
                self.disappeartime = None
                engine_io.rumble(0.0)
                self.appear()


class Menu(Rectangle2DNode):
    def __init__(self):
        super().__init__(self)
        self.layer = 3
        self.color = menucolor
        self.opacity = 0
        self.width, self.height = 130, 130
        
        self.selected = 0
        self.entries = [
            [[Text2DNode(font=font, color=textcolor, layer=4, text="Return")], self._return],
            [[Text2DNode(font=font, color=textcolor, layer=4, text="Quit")], self._quit],
            [[Text2DNode(font=font, color=textcolor, layer=4, text="Rumble Strength:"), Text2DNode(font=font, color=textcolor, layer=4, text="")], self._rumble],
            [[Text2DNode(font=font, color=textcolor, layer=4, text="Special Responses:"), Text2DNode(font=font, color=textcolor, layer=4, text="")], self._rarity],
        ]
        linecount = sum(len(i[0]) for i in self.entries) + len(self.entries)-1
        print(linecount)
        fontheight = 8
        ypos = -linecount*fontheight/2 + fontheight/2
        for i in self.entries:
            for j in i[0]:
                j.position = Vector2(0, ypos)
                j.opacity = self.opacity
                ypos += fontheight
            ypos += fontheight
            i[1](entry=i) #run callback to update text
        
        self._update()
    
    def toggle(self):
        self.opacity ^= 1
        for i in self.entries:
            for j in i[0]:
                j.opacity = self.opacity
    
    def press(self, button):
        entry = self.entries[self.selected]
        entry[1](entry, button=button)
    
    def move(self, direction):
        self.selected += direction
        self.selected %= len(self.entries)
        self._update()
    
    def _return(self, entry=None, button=None):
        if button == 0:
            self.toggle()
    
    def _quit(self, entry=None, button=None):
        global mainloop
        if button == 0:
            mainloop = False
    
    def _rumble(self, entry=None, button=None):
        global vibstrength, rumblesetting
        if button == 1: #left
            rumblesetting -= 1
            if rumblesetting < 0: rumblesetting = 0
        elif button == 2: #right
            rumblesetting += 1
            if rumblesetting >= len(rumbledata): rumblesetting = len(rumbledata)-1
        vibstrength = rumbledata[rumblesetting][1]
        entry[0][1].text = rumbledata[rumblesetting][0]
    
    def _rarity(self, entry=None, button=None):
        global rarity, raritysetting
        if button == 1: #left
            raritysetting -= 1
            if raritysetting < 0: raritysetting = 0
        elif button == 2: #right
            raritysetting += 1
            if raritysetting >= len(raritydata): raritysetting = len(raritydata)-1
        rarity = raritydata[raritysetting][1]
        entry[0][1].text = raritydata[raritysetting][0]
    
    def _update(self):
        for i in self.entries:
            for j in i[0]:
                j.color = textcolor
        for i in self.entries[self.selected][0]:
            i.color = textcolor_selected


#each entry is [text, orientation (False = point up, True = point down), scale multiplier, vertical offset (pixels)]
responses = [
    ["It\nis\ncertain", False, 1.3, 0], #positive
    ["It is\ndecidedly\nso", False, 1, 0],
    ["Without\na doubt", False, 1, 0],
    ["Yes\ndefinitely", False, 1, 0],
    ["You\nmay rely\non it", False, 1, 0],
    ["As I\nsee it,\nyes", False, 1, 0],
    ["Most\nlikely", False, 1.3, 0],
    ["Outlook\ngood", True, 1.3, 0],
    ["Yes", True, 2.3, 0],
    ["Signs\npoint\nto yes", False, 1.3, 0],
    ["Reply\nhazy,\ntry again", False, 1, 0], #neutral
    ["Ask\nagain\nlater", False, 1.3, 0],
    ["Better\nnot tell\nyou now", False, 1, 0],
    ["Cannot\npredict \nnow", True, 1, 0],
    ["Concentrate\n\nand ask\n\nagain", True, 1, 0],
]

responses_negative = [
    ["Don't\ncount\non it", False, 1.3, 3], #negative
    ["My\nreply\nis no", False, 1.3, 0],
    ["My\nsources\nsay no", False, 1.3, 0],
    ["Outlook\nnot so\ngood", True, 1.3, 0],
    ["Very\ndoubtful", False, 1, 0],
]

responses_rare = [
    ["Ask\nKen", False, 2.0, 0],
    ["Fizz\nBuzz", False, 1.3, 0],
    ["foobar", False, 1.3, 0],
    ["Flip a\ncoin", True, 1.3, 0],
    ["How\nshould\nI know?", False, 1.3, 0],
    ["Help!\nI'm\ntrapped\nin a toy\nfactory!", False, 1, 0],
    ["xyzzy", False, 1.3, 0],
    ["Stop\nshaking\nme!", False, 1.3, 0],
    ["Google\nit", True, 1.3, 0],
    ["Huh?", False, 2, 0],
    ["What?", False, 1.3, 0],
    ["I\nhave\nno clue", False, 1.3, 0],
    ["Beats\nme", True, 1.3, 0],
    ["42", False, 3, 0],
    ["I\ndidn't\nsign up\nfor this", False, 1, 0],
    ["You\ndon't\nwant\nto know", False, 1.3, 0],
    ["Leave me\nout of\nthis!", True, 1.3, 0],
    ["Yes!\nWait, No!\nNever mind!", False, 1, 7],
    ["Go\nask\na real\nperson", False, 1.3, 0],
    ["...\n\nSeriously?", False, 1, 0],
    ["404\nNot\nFound", False, 1.3, 0],
    ["Oh\nno\nnot\nthis\nagain", False, 1.3, -7],
    ["Please do\nnot press\nthis\nbutton\nagain", True, 1, 0],
    ["Wake\nup", True, 2, 0],
    ["Behind\nyou", True, 1.3, 0],
    ["Don't\nblink", False, 1.3, 0],
    ["Run!", False, 2, 3],
    ["wat", False, 2, 0],
    ["IDK", False, 2, 0],
    ["Breathe", False, 1, 0],
    ["The\nGame", False, 2, 5],
    ["You've\ngot\nmail!", True, 1.3, 0],
    ["Fingers\ncrossed", False, 1, 0],
    ["Someone\nneeds a\ncookie", True, 1, 0],
    #["We've been trying to reach you about your car's extended warranty", False, 1, 0],
    ["Never\ngonna\ngive you\nup, never\ngonna let\nyou down", False, 1, 0],
    ["Do or\ndo not,\nthere\nis no try", False, 1, 0],
    ["Gonna have\nto sleep\non that\none", True, 1, 0],
    ["I'm too\ntired\nfor\nthis", True, 1.3, 0],
    ["Yesn't", False, 1.3, 0],
    ["The\ndog\nate my\nanswer", False, 1.3, 0],
]

responses += responses_negative #could be added twice to have equal chance of positive and negative responses

menu = Menu()

magic8 = Magic8()
magic8.appear()
magic8.shake()

mainloop = True
while mainloop:
    if not engine.tick():
        continue
    
    if menu.opacity == 0:
        if engine_io.A.is_just_pressed:
            #magic8.appear()
            magic8.shake()
    
    else:
        if engine_io.A.is_just_pressed: menu.press(0)
        if engine_io.LEFT.is_just_pressed: menu.press(1)
        if engine_io.RIGHT.is_just_pressed: menu.press(2)
        if engine_io.UP.is_just_pressed: menu.move(-1)
        if engine_io.DOWN.is_just_pressed: menu.move(1)
        
    
    if engine_io.RB.is_just_pressed:
        print(f"{engine.get_running_fps()} FPS")
        
    if engine_io.LB.is_just_pressed:
        printmem()
    
    if engine_io.B.is_just_pressed or engine_io.MENU.is_just_pressed:
        menu.toggle()

if rumblesetting != engine_save.load("rumble", 4): #save settings if they have changed
    print("Saving rumble setting")
    engine_save.save("rumble", rumblesetting)
if raritysetting != engine_save.load("rarity", 3):
    print("Saving rarity setting")
    engine_save.save("rarity", raritysetting)