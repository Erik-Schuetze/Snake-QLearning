import sys
import random

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QFont

from pynput import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow

window_active = False
active = True

gamestate = []
snake = []
apple_pos = []
apple = False
eaten = False
lost = False
score = 0

size = 10
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
        update_loop(False)
        AI()
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
            if i == 0:
                qp.fillRect((x * rect_size) + 1, (y * rect_size) + 1, rect_size - 2, rect_size - 2, QColor(0, 0, 0))
            else:
                qp.fillRect((x * rect_size) + 1, (y * rect_size) + 1, rect_size - 2, rect_size - 2, QColor(0, color, color))
            i += 1

        qp.end()

def update_loop(debugmode):
    #print("1")
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
    #print(score)
    if debugmode:
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

def init(show_window):
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
    if show_window:
        start_window()
    #else:
    #    while not lost:
            #start_window()
    #        update_loop()
        #time.sleep(0.1)

def set_active(value):
    global active
    active = value


#listener = keyboard.Listener(
#    on_press=on_press,
    #  on_release=on_release)
#)
#listener.start()

#############################################

import random

import numpy as np  # for array stuff and random
from PIL import Image  # for creating visual of our env
#import cv2  # for showing our visual live
import matplotlib.pyplot as plt  # for graphing our mean rewards over time
import pickle  # to save/load Q-Tables
from matplotlib import style  # to make pretty charts because it matters.
import time  # using this to keep track of our saved Q-Tables.



#style.use("ggplot")  # setting our style!


def set_direction(ID):
    global direction
    if ID == 0:
        if not direction == down:
            direction = up
    elif ID == 1:
        if not direction == left:
            direction = right
    elif ID == 2:
        if not direction == up:
            direction = down
    elif ID == 3:
        if not direction == right:
            direction = left

def make_decision():
    decision_ID = 5

    if decision_ID == 5:
        set_direction(random.randint(0, 3))



def AI():
    SIZE = size
    HM_EPISODES = 50000
    MOVE_PENALTY = 1  # feel free to tinker with these!
    LOSE_PENALTY = 300  # feel free to tinker with these!
    FOOD_BASE_REWARD = 300  # feel free to tinker with these!
    FOOD_BONUS_REWARD = 100
    epsilon = 0.5  # randomness
    EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY
    SHOW_EVERY = 1000  # how often to play through env visually.
    MAX_STEPS = 500

    LEARNING_RATE = 0.1
    DISCOUNT = 0.95

    start_q_table = "qtable-1625338052.pickle"

    if start_q_table is None:
        # initialize the q-table
        q_table = {}
        for i in range(-SIZE + 1, SIZE):
            for ii in range(-SIZE + 1, SIZE):
                q_table[i, ii] = [np.random.uniform(-5, 0) for i in range(4)]
    else:
        #print("test")
        with open(start_q_table, "rb") as f:
            q_table = pickle.load(f)
        #print("test2")
    #print(q_table)

    i = 0
    episode_rewards = []
    episode_reward = 0
    EPISODE = 0

    while not lost and i < MAX_STEPS:
        last_score = score
        #make_decision()
        #update_loop(False)
        #print(direction)
        #print("updated")
        #time.sleep(0.01)

        obs = (snake[0][0] - apple_pos[0], snake[0][1] - apple_pos[1])
        # print(obs)
        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)
        # Take the action!
        set_direction(action)
        if lost:
            reward = -LOSE_PENALTY
        elif score == last_score + 1:
            reward = FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * score)
            i = 0
        else:
            reward = -MOVE_PENALTY
        ## NOW WE KNOW THE REWARD, LET'S CALC YO
        # first we need to obs immediately after the move.
        new_obs = (snake[0][0] - apple_pos[0], snake[0][1] - apple_pos[1])
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        if reward == FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * score):
            new_q = FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * score)
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q

        episode_reward += reward
        #if reward == FOOD_REWARD or reward == -LOSE_PENALTY:
        #    break
        episode_score = score
        i += 1

            #if score > last_score:
            #    print("score: " + str(score))

            # print(episode_reward)

    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

    #update_loop(False)
    EPISODE += 1

    #score_visual = "I" * last_score
    #print("Episode: " + str(EPISODE) + ", \treward: " + str(episode_reward)+ ", \tscore: " + str(episode_score) + "\t" + score_visual)



    #moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

    #plt.plot([i for i in range(len(moving_avg))], moving_avg)
    #plt.ylabel(f"Reward {SHOW_EVERY}ma")
    #plt.xlabel("episode #")
    #plt.show()

    #with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    #    pickle.dump(q_table, f)

init(True)