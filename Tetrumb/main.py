import engine_main # type: ignore
import engine # type: ignore
import engine_draw # type: ignore
import engine_io as btn # type: ignore
from engine_io import rumble # type: ignore
from engine_resources import TextureResource as txtr, FontResource as font # type: ignore
from engine_draw import Color, set_background # type: ignore
from engine_nodes import CameraNode, Sprite2DNode as sprt, Text2DNode as text # type: ignore
from engine_math import Vector2, Vector3 # type: ignore
import engine_save # type: ignore
import math
import framebuf # type: ignore
import random

engine_save.set_location("save.data")

engine.fps_limit(30)

camera = CameraNode(position = Vector3(63, 63, 0))

mapTxtr = txtr("/Games/Tetrumb/textures/map.bmp")
redTxtr = txtr("/Games/Tetrumb/textures/red.bmp")
orangeTxtr = txtr("/Games/Tetrumb/textures/orange.bmp")
yellowTxtr = txtr("/Games/Tetrumb/textures/yellow.bmp")
greenTxtr = txtr("/Games/Tetrumb/textures/green.bmp")
cyanTxtr = txtr("/Games/Tetrumb/textures/cyan.bmp")
blueTxtr = txtr("/Games/Tetrumb/textures/blue.bmp")
purpleTxtr = txtr("/Games/Tetrumb/textures/purple.bmp")
shapeTxtr = txtr("/Games/Tetrumb/textures/shape.bmp")

fontTxtr = font("/Games/Tetrumb/textures/5x7Font.bmp")

screen = txtr(128, 128, 0, 16)

shapeView = sprt(position = Vector2(90, 84),
                texture = shapeTxtr,
                transparent_color = Color(0, 0, 0),
                fps = 0,
                frame_count_x = 8,
                layer = 10)

topTxt = text(position = Vector2(95, 22),
           font = fontTxtr,
           text = "000000",
           scale = Vector2(1, 1),
           letter_spacing = 1,
           color = Color(1, 1, 1),
           layer = 10)
scoreTxt = text(position = Vector2(95, 46),
           font = fontTxtr,
           text = "000000",
           scale = Vector2(1, 1),
           letter_spacing = 1,
           color = Color(1, 1, 1),
           layer = 10)
levelTxt = text(position = Vector2(89, 107),
           font = fontTxtr,
           text = "0",
           scale = Vector2(1, 1),
           letter_spacing = 1,
           color = Color(1, 1, 1),
           layer = 10)

def color(r,g,b):
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565
          
fb = engine_draw.front_fb()
#fbuf = framebuf.FrameBuffer(bytearray(128 * 128 * 2), 128, 128, framebuf.RGB565)
fbuf = framebuf.FrameBuffer(screen.data, 128, 128, framebuf.RGB565)
image = framebuf.FrameBuffer(mapTxtr.data, mapTxtr.width, mapTxtr.height, framebuf.RGB565)
fbuf.blit(image,0,0)
red = framebuf.FrameBuffer(redTxtr.data, redTxtr.width, redTxtr.height, framebuf.RGB565)
orange = framebuf.FrameBuffer(orangeTxtr.data, orangeTxtr.width, orangeTxtr.height, framebuf.RGB565)
yellow = framebuf.FrameBuffer(yellowTxtr.data, yellowTxtr.width, yellowTxtr.height, framebuf.RGB565)
green = framebuf.FrameBuffer(greenTxtr.data, greenTxtr.width, greenTxtr.height, framebuf.RGB565)
cyan = framebuf.FrameBuffer(cyanTxtr.data, cyanTxtr.width, cyanTxtr.height, framebuf.RGB565)
blue = framebuf.FrameBuffer(blueTxtr.data, blueTxtr.width, blueTxtr.height, framebuf.RGB565)
purple = framebuf.FrameBuffer(purpleTxtr.data, purpleTxtr.width, purpleTxtr.height, framebuf.RGB565)

Screen = sprt(position = Vector2(63, 63),
            texture = screen,
            layer = 1)
            
grid = [[8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [8,0,0,0,0,0,0,0,0,0,0,8,8],
        [0,8,8,8,8,8,8,8,8,8,8,0,0]]

frame = 0
posX = 5
posY = 2
shape = random.randint(1, 7)
nextShape = random.randint(1, 7)
angle = 0
rumb = 0
line = 0
clears = 0
level = 0
levels = 0
top = 0
score = 0

top = int(engine_save.load("highscore", 0))

box1 = [0, 0]
box2 = [0, 0]
box3 = [0, 0]
box4 = [0, 0]
tetra = [box1, box2, box3, box4]

def draw():
    fbuf.rect(13, 0, 60, 121, color(0, 0, 0), 1)
    for y in range(3, len(grid) - 1):
        for x in range(1, len(grid[y]) - 2):
            if grid[y][x] == 1:
                fbuf.blit(red, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 2:
                fbuf.blit(orange, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 3:
                fbuf.blit(yellow, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 4:
                fbuf.blit(green, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 5:
                fbuf.blit(cyan, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 6:
                fbuf.blit(blue, x * 6 + 7, y * 6 - 17)
            if grid[y][x] == 7:
                fbuf.blit(purple, x * 6 + 7, y * 6 - 17)

def move():
    global shape
    global angle
    global box1
    global box2
    global box3
    global box4

    if shape == 1:
        if angle == 0 or angle == 2:
            box1[0] = posX - 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY - 1

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY
        elif angle == 1 or angle == 3:
            box1[0] = posX + 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX
            box4[1] = posY + 1

    elif shape == 2:
        if angle == 2:
            box1[0] = posX + 1
            box1[1] = posY - 1

            box2[0] = posX - 1
            box2[1] = posY

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY
        elif angle == 3:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX
            box3[1] = posY + 1

            box4[0] = posX + 1
            box4[1] = posY + 1
        elif angle == 0:
            box1[0] = posX - 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY - 1

            box3[0] = posX + 1
            box3[1] = posY - 1

            box4[0] = posX - 1
            box4[1] = posY
        elif angle == 1:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX + 1
            box2[1] = posY - 1

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY + 1

    elif shape == 3:
        box1[0] = posX
        box1[1] = posY - 1

        box2[0] = posX + 1
        box2[1] = posY - 1

        box3[0] = posX
        box3[1] = posY

        box4[0] = posX + 1
        box4[1] = posY

    elif shape == 4:
        if angle == 0 or angle == 2:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX + 1
            box2[1] = posY - 1

            box3[0] = posX - 1
            box3[1] = posY

            box4[0] = posX
            box4[1] = posY
        elif angle == 1 or angle == 3:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY + 1

    elif shape == 5:
        if angle == 0 or angle == 2:
            box1[0] = posX - 1
            box1[1] = posY

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX + 2
            box4[1] = posY
        elif angle == 1 or angle == 3:
            box1[0] = posX
            box1[1] = posY - 2

            box2[0] = posX
            box2[1] = posY - 1

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX
            box4[1] = posY + 1

    elif shape == 6:
        if angle == 2:
            box1[0] = posX - 1
            box1[1] = posY - 1

            box2[0] = posX - 1
            box2[1] = posY

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY
        elif angle == 3:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX + 1
            box2[1] = posY - 1

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX
            box4[1] = posY + 1
        elif angle == 0:
            box1[0] = posX - 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY - 1

            box3[0] = posX + 1
            box3[1] = posY - 1

            box4[0] = posX + 1
            box4[1] = posY
        elif angle == 1:
            box1[0] = posX + 1
            box1[1] = posY - 1

            box2[0] = posX + 1
            box2[1] = posY

            box3[0] = posX
            box3[1] = posY + 1

            box4[0] = posX + 1
            box4[1] = posY + 1

    elif shape == 7:
        if angle == 2:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX - 1
            box2[1] = posY

            box3[0] = posX
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY
        elif angle == 3:
            box1[0] = posX
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX
            box4[1] = posY + 1
        elif angle == 0:
            box1[0] = posX - 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY - 1

            box3[0] = posX + 1
            box3[1] = posY - 1

            box4[0] = posX
            box4[1] = posY
        elif angle == 1:
            box1[0] = posX + 1
            box1[1] = posY - 1

            box2[0] = posX
            box2[1] = posY

            box3[0] = posX + 1
            box3[1] = posY

            box4[0] = posX + 1
            box4[1] = posY + 1

def clear():
    global grid
    global rumb
    global line
    global clears
    global level
    global score
    lvl = 0
    for row in range(len(grid)):
        if min(grid[row]) != 0:
            fbuf.rect(13, row * 6 - 17, 60, 6, color(200, 200, 200), 1)
            grid.pop(row)
            grid.insert(0, [8,0,0,0,0,0,0,0,0,0,0,8,8])
            rumb = frame + 2
            rumble(.4)
            line = frame
            clears += 1
            if clears % 10 == 0:
                level += 1
            lvl += 1
    if lvl == 1:
        score += 100 + round(level * 100 / 10)
    elif lvl == 2:
        score += 300 + round(level * 300 / 10)
    elif lvl == 3:
        score += 525 + round(level * 525 / 10)
    elif lvl >= 4:
        score += 800 + round(level * 800 / 10)


while True:
    if engine.tick():

        frame += 1
        if frame >= rumb + 2:
            rumble(0)

        if frame <= line + 8:
            fb.blit(fbuf,0,0)
            continue

        draw()
        move()

        levels = level
        if levels > 10:
            levels = 10

        for box in tetra:
            if shape == 1:
                fbuf.blit(red, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 2:
                fbuf.blit(orange, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 3:
                fbuf.blit(yellow, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 4:
                fbuf.blit(green, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 5:
                fbuf.blit(cyan, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 6:
                fbuf.blit(blue, box[0] * 6 + 7, box[1] * 6 - 17)
            elif shape == 7:
                fbuf.blit(purple, box[0] * 6 + 7, box[1] * 6 - 17)


        if btn.MENU.is_just_pressed:
            rumble(0)
            levels = -1
            break
        elif btn.B.is_just_pressed:
            if angle > 0:
                angle -= 1
            else:
                angle = 3
            move()
            if (grid[box1[1]][box1[0]] != 0
            or grid[box2[1]][box2[0]] != 0
            or grid[box3[1]][box3[0]] != 0
            or grid[box4[1]][box4[0]] != 0):
                if angle < 3:
                    angle += 1
                else:
                    angle = 0
                move()
        elif btn.A.is_just_pressed:
            if angle < 3:
                angle += 1
            else:
                angle = 0
            move()
            if (grid[box1[1]][box1[0]] != 0
            or grid[box2[1]][box2[0]] != 0
            or grid[box3[1]][box3[0]] != 0
            or grid[box4[1]][box4[0]] != 0):
                if angle > 0:
                    angle -= 1
                else:
                    angle = 3
                move()
        elif btn.LEFT.is_just_pressed:
            if (grid[box1[1]][box1[0] - 1] == 0
            and grid[box2[1]][box2[0] - 1] == 0
            and grid[box3[1]][box3[0] - 1] == 0
            and grid[box4[1]][box4[0] - 1] == 0):
                posX -= 1
                move()
        elif btn.LEFT.is_long_pressed:
            if frame % 3 == 0:
                if (grid[box1[1]][box1[0] - 1] == 0
                and grid[box2[1]][box2[0] - 1] == 0
                and grid[box3[1]][box3[0] - 1] == 0
                and grid[box4[1]][box4[0] - 1] == 0):
                    posX -= 1
                    move()
        elif btn.RIGHT.is_just_pressed:
            if (grid[box1[1]][box1[0] + 1] == 0
            and grid[box2[1]][box2[0] + 1] == 0
            and grid[box3[1]][box3[0] + 1] == 0
            and grid[box4[1]][box4[0] + 1] == 0):
                posX += 1
                move()
        elif btn.RIGHT.is_long_pressed:
            if frame % 3 == 0:
                if (grid[box1[1]][box1[0] + 1] == 0
                and grid[box2[1]][box2[0] + 1] == 0
                and grid[box3[1]][box3[0] + 1] == 0
                and grid[box4[1]][box4[0] + 1] == 0):
                    posX += 1
                    move()
                

        if btn.DOWN.is_just_pressed:
                rumb = frame
                rumble(.5)
        if btn.DOWN.is_pressed:
            if frame % 2 == 0:
                if (grid[box1[1] + 1][box1[0]] == 0
                and grid[box2[1] + 1][box2[0]] == 0
                and grid[box3[1] + 1][box3[0]] == 0
                and grid[box4[1] + 1][box4[0]] == 0):
                    posY += 1
                    score += .5 + (level / 10)
                else:
                    for box in tetra:
                        grid[box[1]][box[0]] = shape
                    posX = 5
                    posY = 2
                    shape = nextShape
                    nextShape = random.randint(1, 7)
                    if shape == nextShape:
                        nextShape = random.randint(1, 7)
                    rumb = frame + 1
                    rumble(.5)
                    clear()
                    angle = 0
        elif frame % (15 - levels) == 0:
            if (grid[box1[1] + 1][box1[0]] == 0
            and grid[box2[1] + 1][box2[0]] == 0
            and grid[box3[1] + 1][box3[0]] == 0
            and grid[box4[1] + 1][box4[0]] == 0):
                posY += 1
            else:
                for box in tetra:
                    grid[box[1]][box[0]] = shape
                posX = 5
                posY = 2
                shape = nextShape
                nextShape = random.randint(1, 7)
                if shape == nextShape:
                    nextShape = random.randint(1, 7)
                rumb = frame + 1
                rumble(.5)
                clear()
                angle = 0
        
        shapeView.frame_current_x = nextShape
        
        topTxt.text = str(top)
        scoreTxt.text = str(round(score))
        levelTxt.text = str(level)
        
        if grid[2] != [8,0,0,0,0,0,0,0,0,0,0,8,8]:
            levelTxt.text = str('OVER')
            rumble(0)
            break

        fb.blit(fbuf,0,0)
        engine.tick()
        
if score >= top:
    engine_save.save("highscore", round(score))

while True:
    if engine.tick():

        if btn.MENU.is_just_pressed:
            rumble(0)
            break
        if levels == -1:
            break

        #fb.blit(fbuf,0,0)
        engine.tick()














