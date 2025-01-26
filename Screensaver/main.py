import engine_main
import engine
import engine_io
import engine_draw
from engine_resources import FontResource, TextureResource
from engine_nodes import CameraNode, Text2DNode, Sprite2DNode, EmptyNode
from engine_math import Vector2
from engine_animation import Tween, PING_PONG, ONE_SHOT, EASE_LINEAR, EASE_CUBIC_IN

from os import stat, remove

def isfile(path):
    try:
        if stat(path)[0] & 32768: #https://forum.micropython.org/viewtopic.php?t=10957
            return True
        else:
            return False
    except OSError:
        return False

launcherpath = "/system/launcher/launcher.py"
saverpath = "/system/launcher/screensaver.py"

patches = [ #each is an existing line in the launcher, and the new line to be inserted after it.
["from system.launcher.custom_camera import CustomCamera", "from system.launcher.screensaver import ScreenSaver"],
["dynamic_background = DynamicBackground()", "screensaver = ScreenSaver()"],
["camera.add_child(dynamic_background)", "camera.add_child(screensaver)"],
]

def patch(install=False, write=False):
    with open(launcherpath, "r") as f:
        file = f.read().splitlines()
    
    for i in patches: #uninstall any existing patches, ensure compatibility
        if not i[0] in file:
            print("Missing search string")
            return False #search string doesn't exist - launcher is incompatible with installer
        if i[1] in file:
            file.pop(file.index(i[1]))
    
    if "screensaver" in "\n".join(file): #sanity check
        print("Patcher failed to completely remove screensaver")
        return False
    
    if install: #apply patches
        for i in patches:
            file.insert(file.index(i[0])+1, i[1])
    
    if write:
        if isfile(saverpath):
            remove(saverpath)
        if install:
            with open("/Games/Screensaver/screensaver.py", "r") as rf:
                with open(saverpath, "w") as wf:
                    wf.write(rf.read())
        with open(launcherpath, "w") as f:
            f.write("\n".join(file))
    
    return True

#patch(install=False, write=False)

font = FontResource("/Games/Screensaver/SperryPC8x16-1bit.bmp", True)
bg = TextureResource("/Games/Screensaver/bg.bmp", True)

camera = CameraNode()

class Disclaimer(EmptyNode):
    def __init__(self):
        super().__init__(self)
        self.opacity = 0.0
        self.text = [
            Text2DNode(font=font, color=engine_draw.yellow, text="WARNING:"),
            Text2DNode(font=font, text="This modifies"),
            Text2DNode(font=font, text="critical system"),
            Text2DNode(font=font, text="files. Read the"),
            Text2DNode(font=font, text="readme before"),
            Text2DNode(font=font, text="installation."),
        ]
        for num, i in enumerate(self.text):
            i.position = Vector2(0, 16*num - 16*len(self.text)/2 + 8)
            self.add_child(i)
        
        self.flasher = Text2DNode(font=font, text="A", opacity=1.0, position=Vector2(55,55))
        self.add_child(self.flasher)
        self.flashtween = Tween()
        self.flashtween.start(self.flasher, "opacity", 1.0, 0.0, 1000, 1.0, PING_PONG, EASE_LINEAR)
        
        self.tween = Tween()
        self.tween.start(self, "opacity", 0.0, 1.0, 1000, 1.0, ONE_SHOT, EASE_CUBIC_IN)
    
    def hide(self, after=None):
        if self.opacity < 1: return
        if after != None:
            self.tween.after = after
        self.tween.start(self, "opacity", 1.0, 0.0, 200, 1.0, ONE_SHOT, EASE_LINEAR)

class Menu(Sprite2DNode):
    def __init__(self):
        super().__init__(self)
        self.texture = bg
        self.opacity = 0.0
        self.text = [
            Text2DNode(font=font, layer=1, text="Install"),
            Text2DNode(font=font, layer=1, text="Uninstall"),
            Text2DNode(font=font, layer=1, text="Exit"),
            Text2DNode(font=font, layer=1, color=engine_draw.darkgrey, text="..."),
        ]
        for num, i in enumerate(self.text):
            i.position = Vector2(0, 16*num - 16*len(self.text)/2 + 8)
            self.add_child(i)
        if not patch(install=True): #initial compatibility check
            self.text[-1].color = engine_draw.red
            self.text[-1].text = "Can't edit file!"
        
        self.selection = 0
        self.move(0)
    
    def move(self, direction):
        self.text[self.selection].color = engine_draw.white
        self.selection += direction
        self.selection %= 3
        self.text[self.selection].color = engine_draw.skyblue
    
    def select(self):
        global mainloop
        if self.selection == 0:
            if patch(install=True, write=True):
                self.text[-1].color = engine_draw.green
                self.text[-1].text = "Installed!"
            else:
                self.text[-1].color = engine_draw.red
                self.text[-1].text = "Install failed!"
        elif self.selection == 1:
            if patch(install=False, write=True):
                self.text[-1].color = engine_draw.green
                self.text[-1].text = "Uninstalled!"
            else:
                self.text[-1].color = engine_draw.red
                self.text[-1].text = "Uninstall failed"
        elif self.selection == 2:
            mainloop = False
    
    def show(self, dummy=None):
        if self.opacity > 0: return
        self.tween = Tween()
        self.tween.start(self, "opacity", 0.0, 1.0, 200, 1.0, ONE_SHOT, EASE_LINEAR)

disclaimer = Disclaimer()
menu = Menu()

mainloop = True
while mainloop:
    if not engine.tick():
        continue
    if not menu.opacity > 0:
        if engine_io.A.is_just_pressed: disclaimer.hide(menu.show)
    else:
        if engine_io.A.is_just_pressed: menu.select()
        if engine_io.UP.is_just_pressed: menu.move(-1)
        if engine_io.DOWN.is_just_pressed: menu.move(1)
    if engine_io.B.is_just_pressed: break
