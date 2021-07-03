import time
import os
import sys
import random
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QDir, QUrl
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog

window_active = False
active = True

gamestate = []
snake = []
apple_pos = []
apple = False
eaten = False
lost = False
score = 0

size = 15
width = size
height = size
window_height = height * 30
window_width = width * 30
ui_width = 300

up = (0, -1)
down = (0, +1)
left = (-1, 0)
right = (+1, 0)

direction = right


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, window_width + ui_width, window_height)
        self.setWindowTitle("SCHNYBERPUNK 2077")
        self.show()


        self.timer = QTimer()
        self.timer.timeout.connect(self.call_loop)

        self.timer.start(100)

# ---------------- video part

#        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
#        videoWidget = QVideoWidget()

#        wid = QWidget(self)
#        self.setCentralWidget(videoWidget)

        #layout = QVBoxLayout()
        #layout.addWidget(videoWidget)

        #wid.setLayout(layout)

#        self.mediaPlayer.setVideoOutput(videoWidget)
#

#        #fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
#        fileName = "C:/Users/eschuetze/Desktop/Snake.mp4"
#        #print(fileName, _)
#

#        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
#        print(self.mediaPlayer.errorString())
#        print("test")
#        self.mediaPlayer.play()
#        print("test")


# -------------- video part

    def call_loop(self):
        update_loop()
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        rect_size = 30
        steps_width = window_width // rect_size
        steps_height = window_height // rect_size

        global score
        text = "Score: " + str(score)
        qp.setFont(QFont("Arial", 20))
        qp.drawText(window_width + (ui_width//6), window_height//6, text)

        for y in range(0, steps_height):
            for x in range(0, steps_width):
                checkerboard = (y + x) % 2
                if checkerboard == 1:
                    qp.fillRect(x * rect_size, y * rect_size, rect_size, rect_size, QColor(235, 235, 235))
                elif checkerboard == 0:
                    qp.fillRect(x * rect_size, y * rect_size, rect_size, rect_size, QColor(230, 230, 230))


                #if gamestate[x][y] == 3:
                    #qp.fillRect((x * rect_size) - 1, (y * rect_size) - 1, rect_size + 1, rect_size + 1, QColor(200, 0, 0))

        global apple_pos
        (x, y) = apple_pos
        qp.fillRect((x * rect_size) + 5, (y * rect_size) + 5, rect_size - 10, rect_size - 10, QColor(200, 0, 0))

        global snake
        i = 0
        while i < len(snake):
            (x, y) = snake[i]
            color_multiplier = 1 / len(snake)
            color = ((i * color_multiplier) * 70) + 30
            color = round(color)
            qp.fillRect((x * rect_size) + 1, (y * rect_size) + 1, rect_size - 2, rect_size - 2, QColor(0, color, color))
            i += 1

        qp.end()

def update_loop():
    print("1")
    check_lost()
    #print("2")
    spawn_apple()
    #print("3")
    eat()
    #print("4")
    movement()
    #print("5")
    update_score()
    #clear_gamestate()
    update_gamestate()
    #print("6")
    print_gamestate()
    #print(snake)

#-------------------------------------
def print_gamestate():
    global gamestate
    print("")
    output = ""
    for line in gamestate:
        print(line)

def check_lost():
    global lost
    if lost:
        #print("lost")
        clear_gamestate()
        set_snake()
        spawn_apple()
        lost = not lost

def update_score():
    global score
    score = len(snake) - 2

def get_head_pos():
    global snake
    x = snake[0][0]
    y = snake[0][1]
    return (x, y)

def check_apple():
    global gamestate
    for y in range(0, height):
        for x in range(0, width):
            if gamestate[x][y] == 3:
                return True
    return False

def eat():
    global apple
    global eaten
    if not check_apple():
        #print("apfel gone")
        apple = not apple
        eaten = not eaten



def movement():
    global gamestate
    global snake
    global eaten
    global lost

    head_x = snake[0][0]
    head_y = snake[0][1]
    #gamestate[head_x][head_y] = 2

    (offset_x, offset_y) = direction
    new_x = head_x + offset_x
    new_y = head_y + offset_y


    if ((0 <= new_x and new_x <= width - 1) and (0 <= new_y and new_y <= height - 1)):
        #gamestate[new_x][new_y] = 1
        i = 1
        snake[0] = [new_x, new_y]
        old_pos = head_x, head_y
        while i < len(snake):
            old_x = snake[i][0]
            old_y = snake[i][1]
            snake[i] = old_pos
            old_pos = [old_x, old_y]
            if eaten and i == (len(snake) - 1):
                snake.append(old_pos)
                eaten = not eaten
            i+=1
    else:
        gamestate[head_x][head_y] = 1
        lost = True

    if check_collision():
        lost = True

def check_collision():
    global snake
    i = 1
    collided = False

    while i < len(snake):
        if snake[0] == snake[i]:
            collided = True
        i+=1

    if collided:
        return True
    else:
        return False

def spawn_apple():
    global apple
    global apple_pos

    while not apple:
        spawn_x = random.randint(0, width - 1)
        spawn_y = random.randint(0, height - 1)
        if gamestate[spawn_x][spawn_y] == 0:
            apple_pos = [spawn_x, spawn_y]
            gamestate[spawn_x][spawn_y] = 3
            apple = not apple

def start_window():
    app = QApplication(sys.argv)
    global window
    window = Window()
    window.show()
    sys.exit(app.exec())


def set_snake():
    global snake
    global direction
    global gamestate

    snake = []
    array = [width // 2, height // 2]
    snake.append(array)
    gamestate[array[0]][array[1]] = 1

    array[0] = array[0] - 1
    snake.append(array)
    gamestate[array[0]][array[1]] = 2

    direction = right

def clear_gamestate():
    global gamestate
    for y in range(0, height):
        for x in range(0, width):
            gamestate[x][y] = 0
    global apple
    global eaten
    global apple_pos
    apple = False
    eaten = False
    apple_pos = []

def on_press(key):
    global direction
    try:
        if key.char == "w":
            if not direction == down:
                direction = up
        if key.char == "a":
            if not direction == right:
                direction = left
        if key.char == "s":
            if not direction == up:
                direction = down
        if key.char == "d":
            if not direction == left:
                direction = right
    except:
        print("please use WASD")

def update_gamestate():
    global gamestate
    global apple_pos

    for y in range(0, height):
        for x in range(0, width):
            gamestate[x][y] = 0

    (x, y) = apple_pos
    gamestate[x][y] = 3

    i = 0
    while i < len(snake):
        (x, y) = snake[i]
        if i == 0:
            gamestate[x][y] = 1
        else:
            gamestate[x][y] = 2
        i+=1

def init(window_bool):
    # INIT EMPTY GAMESTATE
    global gamestate

    for x in range(0, width):
        line_array = []
        for y in range(0, height):
            line_array.append(0)
        gamestate.append(line_array)

    set_snake()
    spawn_apple()

    global window_active
    if window_bool:
        start_window()
    #else:
    #    while not lost:
            #start_window()
    #        update_loop()
        #time.sleep(0.1)

def set_active(value):
    global active
    active = value

listener = keyboard.Listener(
    on_press=on_press,
    #on_release=on_release)
)
listener.start()

#window_active = True

#init(window_active)

######################
# Q PART STARTS HERE #
######################


