import random

import numpy as np  # for array stuff and random
from PIL import Image  # for creating visual of our env
#import cv2  # for showing our visual live
import matplotlib.pyplot as plt  # for graphing our mean rewards over time
import pickle  # to save/load Q-Tables
from matplotlib import style  # to make pretty charts because it matters.
import time  # using this to keep track of our saved Q-Tables.

import main

style.use("ggplot")  # setting our style!

SIZE = main.size
HM_EPISODES = 10
MOVE_PENALTY = 1  # feel free to tinker with these!
ENEMY_PENALTY = 300  # feel free to tinker with these!
FOOD_REWARD = 25  # feel free to tinker with these!
epsilon = 0.5  # randomness
EPS_DECAY = 0.9999  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 1000  # how often to play through env visually.

LEARNING_RATE = 0.1
DISCOUNT = 0.95

AI_Mode = True
init_param = not AI_Mode

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
        main.direction = main.up
    elif ID == 1:
        main.direction = main.right
    elif ID == 2:
        main.direction = main.down
    elif ID == 3:
        main.direction = main.left

main.init(init_param)

print(main.gamestate)

EPISODE = 0
while EPISODE < HM_EPISODES:
    while not main.lost:
        set_direction(random.randint(0,3))
        main.update_loop()
        print(main.direction)
        time.sleep(1)
    main.update_loop()
    print("Episode: " + str(EPISODE))
    EPISODE+=1


