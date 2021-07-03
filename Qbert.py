import random

import numpy as np  # for array stuff and random
from PIL import Image  # for creating visual of our env
#import cv2  # for showing our visual live
import matplotlib.pyplot as plt  # for graphing our mean rewards over time
import pickle  # to save/load Q-Tables
from matplotlib import style  # to make pretty charts because it matters.
import time  # using this to keep track of our saved Q-Tables.

import schnyberpunk2077 as snake

style.use("ggplot")  # setting our style!

SIZE = snake.size
HM_EPISODES = 1000
MOVE_PENALTY = 1  # feel free to tinker with these!
ENEMY_PENALTY = 300  # feel free to tinker with these!
FOOD_REWARD = 25  # feel free to tinker with these!
epsilon = 0.5  # randomness
EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 1000  # how often to play through env visually.

LEARNING_RATE = 0.1
DISCOUNT = 0.95

start_q_table = None

#if start_q_table is None:
    # initialize the q-table#
#    q_table = {}
#    for i in range(-SIZE+1, SIZE):
#        for ii in range(-SIZE+1, SIZE):
#            for iii in range(-SIZE+1, SIZE):
#                    for iiii in range(-SIZE+1, SIZE):
#                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]
#else:
#    with open(start_q_table, "rb") as f:
#        q_table = pickle.load(f)

def set_direction(ID):
    if ID == 0:
        snake.direction = snake.up
    elif ID == 1:
        snake.direction = snake.right
    elif ID == 2:
        snake.direction = snake.down
    elif ID == 3:
        snake.direction = snake.left

snake.init(False)

EPISODE = 0
while EPISODE < HM_EPISODES:
    while not snake.lost:
        set_direction(random.randint(0, 3))
        snake.update_loop()
        print(snake.direction)
        time.sleep(0.1)

    snake.update_loop()
    print("Episode: " + str(EPISODE + 1))
    EPISODE+=1

#thread2.join()



