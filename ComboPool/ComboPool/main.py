import engine_main # type: ignore
import engine # type: ignore
import engine_io as btn # type: ignore
from engine_io import rumble # type: ignore
from engine_resources import TextureResource as txtr # type: ignore
from engine_draw import Color, set_background # type: ignore
from engine_nodes import CameraNode, Sprite2DNode as sprt, PhysicsRectangle2DNode as rectBox, PhysicsCircle2DNode as crclBox# type: ignore
from engine_nodes import Line2DNode as line # type: ignore
from engine_math import Vector2, Vector3 # type: ignore
import math
import framebuf # type: ignore
import random

engine.fps_limit(40)

camera = CameraNode(position = Vector3(63, 63, 0))

tileTxtr = txtr("/Games/ComboPool/textures/Tile.bmp")
ballTxtr = txtr("/Games/ComboPool/textures/Ball.bmp")
shadowTxtr = txtr("/Games/ComboPool/textures/Shadow.bmp")
healthBarTxtr = txtr("/Games/ComboPool/textures/HealthBar.bmp")
endingTxtr = txtr("/Games/ComboPool/textures/Ending.bmp")
titleTxtr = txtr("/Games/ComboPool/textures/Title.bmp")
difficultyTxtr = txtr("/Games/ComboPool/textures/Difficulty.bmp")


def color(r,g,b):
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565

screen = txtr(128, 128, 0, 16)

fbuf = framebuf.FrameBuffer(screen.data, 128, 128, framebuf.RGB565)
fbuf.fill(color(53, 68, 58))
image = framebuf.FrameBuffer(tileTxtr.data, tileTxtr.width, tileTxtr.height, framebuf.RGB565)
fbuf.blit(image, 0, 0, color(255, 255, 255))


set_background(screen)


titleSprt = sprt(position = Vector2(63, 28),
                 texture = titleTxtr,
                 transparent_color = Color(1, 1, 1),
                 opacity = 1,
                 playing = False,
                 layer = 6)

difficultySprt = sprt(position = Vector2(63, 83),
                 texture = difficultyTxtr,
                 transparent_color = Color(1, 1, 1),
                 opacity = 1,
                 playing = False,
                 frame_count_y = 3,
                 layer = 6)

difficulty = 0
end = False

while True:
    if engine.tick():
        engine.tick()
        if btn.MENU.is_just_pressed:
            end = True
            break
        elif btn.UP.is_just_pressed:
            if difficulty > 0:
                difficulty -= 1
        elif btn.DOWN.is_just_pressed:
            if difficulty < 2:
                difficulty += 1
        elif btn.A.is_just_pressed:
            titleSprt.opacity = 0
            difficultySprt.opacity = 0
            break

        difficultySprt.frame_current_y = difficulty


ball1 = crclBox()
ball2 = crclBox()
ball3 = crclBox()
ball4 = crclBox()
ball5 = crclBox()
ball6 = crclBox()
ball7 = crclBox()
ball8 = crclBox()
ball9 = crclBox()
ball10 = crclBox()
ball11 = crclBox()
ball12 = crclBox()
ball13 = crclBox()
ball14 = crclBox()
ball15 = crclBox()
ball16 = crclBox()

ball1Sprt = sprt()
ball2Sprt = sprt()
ball3Sprt = sprt()
ball4Sprt = sprt()
ball5Sprt = sprt()
ball6Sprt = sprt()
ball7Sprt = sprt()
ball8Sprt = sprt()
ball9Sprt = sprt()
ball10Sprt = sprt()
ball11Sprt = sprt()
ball12Sprt = sprt()
ball13Sprt = sprt()
ball14Sprt = sprt()
ball15Sprt = sprt()
ball16Sprt = sprt()

ball1Shadow = sprt()
ball2Shadow = sprt()
ball3Shadow = sprt()
ball4Shadow = sprt()
ball5Shadow = sprt()
ball6Shadow = sprt()
ball7Shadow = sprt()
ball8Shadow = sprt()
ball9Shadow = sprt()
ball10Shadow = sprt()
ball11Shadow = sprt()
ball12Shadow = sprt()
ball13Shadow = sprt()
ball14Shadow = sprt()
ball15Shadow = sprt()
ball16Shadow = sprt()

ball1.add_child(ball1Sprt)
ball2.add_child(ball2Sprt)
ball3.add_child(ball3Sprt)
ball4.add_child(ball4Sprt)
ball5.add_child(ball5Sprt)
ball6.add_child(ball6Sprt)
ball7.add_child(ball7Sprt)
ball8.add_child(ball8Sprt)
ball9.add_child(ball9Sprt)
ball10.add_child(ball10Sprt)
ball11.add_child(ball11Sprt)
ball12.add_child(ball12Sprt)
ball13.add_child(ball13Sprt)
ball14.add_child(ball14Sprt)
ball15.add_child(ball15Sprt)
ball16.add_child(ball16Sprt)

ball1.add_child(ball1Shadow)
ball2.add_child(ball2Shadow)
ball3.add_child(ball3Shadow)
ball4.add_child(ball4Shadow)
ball5.add_child(ball5Shadow)
ball6.add_child(ball6Shadow)
ball7.add_child(ball7Shadow)
ball8.add_child(ball8Shadow)
ball9.add_child(ball9Shadow)
ball10.add_child(ball10Shadow)
ball11.add_child(ball11Shadow)
ball12.add_child(ball12Shadow)
ball13.add_child(ball13Shadow)
ball14.add_child(ball14Shadow)
ball15.add_child(ball15Shadow)
ball16.add_child(ball16Shadow)

balls = [ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8, ball9, ball10, ball11, ball12, ball13, ball14, ball15, ball16]

def circleBox(ball):
    ball.position = Vector2(64, 126)
    ball.radius = 4.5
    ball.density = 1
    ball.outline = False
    ball.gravity_scale = Vector2(0, 0)

def ballSprite(ball):
    ball.position = Vector2(0, 0)
    ball.texture = ballTxtr
    ball.transparent_color = Color(1, 1, 1)
    ball.playing = False
    ball.frame_count_x = 1
    ball.frame_count_y = 7
    ball.layer = 5

def shadowSprite(ball):
    ball.position = Vector2(-1, 2)
    ball.texture = shadowTxtr
    ball.transparent_color = Color(1, 1, 1)
    ball.layer = 2
    
for ball in balls:
    circleBox(ball)
    ballSprite(ball.get_child(0))
    shadowSprite(ball.get_child(1))



aim = line(start = Vector2(63, 126),
           end = Vector2(0, 0),
           thickness = 3,
           color = Color(.129, .176, .322),
           layer = 4)

healthBar = sprt(position = Vector2(63, 1),
                 texture = healthBarTxtr,
                 playing = False,
                 frame_count_x = 1,
                 frame_count_y = 11,
                 layer = 6)

ending = sprt(position = Vector2(63, 59),
              texture = endingTxtr,
              transparent_color = Color(1, 1, 1),
              opacity = 0,
              playing = False,
              frame_count_x = 1,
              frame_count_y = 1,
              layer = 6)

queue = [ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8, ball9, ball10, ball11, ball12, ball13, ball14, ball15, ball16]
angle = 3 * math.pi / 2 + .01
rum = 0
endTimer = 0
gameOver = 0
win = 0


def friction():
    temp = (math.sqrt(ball.velocity.x **2 + ball.velocity.y **2))
    frctn = .02

    if temp > 0:
        if abs(ball.velocity.x) < abs((ball.velocity.x / temp) * frctn):
            ball.velocity.x = 0
        else:
            ball.velocity.x -= (ball.velocity.x / temp) * frctn
        if abs(ball.velocity.y) < abs((ball.velocity.y / temp) * frctn):
            ball.velocity.y = 0
        else:
            ball.velocity.y -= (ball.velocity.y / temp) * frctn

def collide(self, contact):
    global rum
    global win
    if self.dynamic == True:
        if contact.node.dynamic == True:
            vel1 = (math.sqrt(self.velocity.x **2 + self.velocity.y **2))
            vel2 = (math.sqrt(contact.node.velocity.x **2 + contact.node.velocity.y **2))
            if self.get_child(0).frame_current_y == contact.node.get_child(0).frame_current_y:
                rumble(.4)
                rum = 2
                if vel1 > vel2:
                    if self.get_child(0).frame_current_y == 6:
                        self.velocity.x *= 3
                        self.velocity.y *= 3
                        win = 1
                    else:
                        self.get_child(0).frame_current_y += 1

                    contact.node.collision_mask = 1
                    contact.node.disable_collision_layer(0)
                    contact.node.get_child(0).frame_current_y = 0
                    contact.node.dynamic = False
                    contact.node.position = Vector2(64, 126)
                    queue.append(contact.node)



ball1.on_collide = collide
ball2.on_collide = collide
ball3.on_collide = collide
ball4.on_collide = collide
ball5.on_collide = collide
ball6.on_collide = collide
ball7.on_collide = collide
ball8.on_collide = collide
ball9.on_collide = collide
ball10.on_collide = collide
ball11.on_collide = collide
ball12.on_collide = collide
ball13.on_collide = collide
ball14.on_collide = collide
ball15.on_collide = collide
ball16.on_collide = collide

def wall():
    if ball.position.y > 114:
        if ball.velocity.y > 0:
            ball.velocity.y *= -1
    if ball.position.y < 5:
        if ball.velocity.y < 0:
            ball.velocity.y *= -1
    elif ball.position.x < 5:
        if ball.velocity.x < 0:
            ball.velocity.x *= -1
    elif ball.position.x > 122:
        if ball.velocity.x > 0:
            ball.velocity.x *= -1

def trail():
    if ball.velocity.x != 0 or ball.velocity.y != 0:
        if ball.get_child(0).frame_current_y == 0:
            trailColor = color(222, 227, 222)
        elif ball.get_child(0).frame_current_y == 1:
            trailColor = color(255, 235, 41)
        elif ball.get_child(0).frame_current_y == 2:
            trailColor = color(255, 166, 0)
        elif ball.get_child(0).frame_current_y == 3:
            trailColor = color(255, 0, 74)
        elif ball.get_child(0).frame_current_y == 4:
            trailColor = color(107, 53, 156)
        elif ball.get_child(0).frame_current_y == 5:
            trailColor = color(25, 77, 189)
        elif ball.get_child(0).frame_current_y == 6:
            trailColor = color(33, 45, 82)
        fbuf.ellipse(round(ball.position.x), round(ball.position.y), 1, 1, trailColor, 1)

def shuffle():
    ball16.position = Vector2(random.randint(6, 57), random.randint(6, 33))
    ball15.position = Vector2(random.randint(6, 57), random.randint(46, 73))
    ball14.position = Vector2(random.randint(6, 57), random.randint(86, 113))
    ball13.position = Vector2(random.randint(70, 121), random.randint(6, 33))
    ball12.position = Vector2(random.randint(70, 121), random.randint(46, 73))
    ball11.position = Vector2(random.randint(70, 121), random.randint(86, 113))

    for i in range(6):
        queue[-1].collision_mask = 2
        queue[-1].dynamic = True
        queue[-1].get_child(0).frame_current_y = random.randint(0, 2)
        queue.pop(-1)


def reset():
    global gameOver
    global queue
    global endTimer
    global difficulty
    global win
    gameOver = 0
    queue = []
    endTimer = 0
    ending.opacity = 0
    win = 0
    for ball in balls:
        queue.append(ball)
        ball.position = Vector2(63, 126)
        ball.get_child(0).frame_current_y = 0
        ball.dynamic = False
        ball.disable_collision_layer(0)
        ball.collision_mask = 1
    if difficulty == 1:
        queue.pop(0)
        queue.pop(1)
    elif difficulty == 2:
        queue.pop(0)
        queue.pop(1)
        queue.pop(2)
        queue.pop(3)
    shuffle()


for ball in queue:
    ball.dynamic = False
    ball.disable_collision_layer(0)

if difficulty == 1:
        queue.pop(0)
        queue.pop(1)
elif difficulty == 2:
    queue.pop(0)
    queue.pop(1)
    queue.pop(2)
    queue.pop(3)

shuffle()

while True:
    if engine.tick():
        engine.tick()
        
        if end == True:
            break

        if rum > 0:
            rum -= 1
        else:
            rumble(0)

        aim.end = Vector2((63 - math.cos(angle) * -150), (126 - math.sin(angle) * -150))
        healthBar.frame_current_y = len(queue)

        for ball in balls:
            friction()
            wall()
            trail()

        for i in range(8):
            if win == 1:
                fbuf.ellipse(random.randint(3, 124), random.randint(3, 116), 2, 2, color(16, 57, 140), 1)
            elif len(queue) > 0:
                fbuf.ellipse(random.randint(3, 124), random.randint(3, 116), 2, 2, color(53, 68, 58), 1)
            else:
                fbuf.ellipse(random.randint(3, 124), random.randint(3, 116), 2, 2, color(132, 36, 82), 1)
        
        fbuf.blit(image, 0, 0, color(255, 255, 255))

        if len(queue) == 0:
            gameOver = 1
            for ball in balls:
                if ball.velocity.x != 0 or ball.velocity.y != 0:
                    gameOver = 0
                    endTimer = 0
                    break
            if gameOver == 1:
                if endTimer < 80:
                    endTimer += 1
                ending.opacity = endTimer / 80

            
        if btn.MENU.is_pressed:
            rumble(0)
            break
        elif btn.RB.is_pressed:
            if btn.B.is_pressed:
                if angle < 2 * math.pi - .2:
                    angle += .01
            else:
                if angle < 2 * math.pi - .2:
                    angle += .04
        elif btn.LB.is_pressed:
            if btn.B.is_pressed:
                if angle > math.pi + .2:
                    angle -= .01
            else:
                if angle > math.pi + .2:
                    angle -= .04
        if btn.A.is_just_pressed and len(queue) > 0 and win == 0:
            rumble(.4)
            rum = 1
            queue[0].collision_mask = 2
            queue[0].dynamic = True
            queue[0].velocity.x = math.cos(angle) * 5
            queue[0].velocity.y = math.sin(angle) * 5
            queue.pop(0)

        if (gameOver == 1 or win == 1) and btn.A.is_just_pressed:
            reset()
        
        print(engine.get_running_fps())
            





























