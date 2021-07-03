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
HM_EPISODES = 24000
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

start_q_table = None

if start_q_table is None:
    # initialize the q-table
    q_table = {}
    for i in range(-SIZE+1, SIZE):
        for ii in range(-SIZE+1, SIZE):
            q_table[i, ii] = [np.random.uniform(-5, 0) for i in range(4)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

def set_direction(ID):
    if ID == 0:
        if not snake.direction == snake.down:
            snake.direction = snake.up
    elif ID == 1:
        if not snake.direction == snake.left:
            snake.direction = snake.right
    elif ID == 2:
        if not snake.direction == snake.up:
            snake.direction = snake.down
    elif ID == 3:
        if not snake.direction == snake.right:
            snake.direction = snake.left

def make_decision():
    decision_ID = 5

    if decision_ID == 5:
        set_direction(random.randint(0, 3))

snake.init(False)

episode_rewards = []
EPISODE = 0
while EPISODE < HM_EPISODES:
    episode_reward = 0
    i = 0

    while not snake.lost and i < MAX_STEPS:
        last_score = snake.score
        #make_decision()
        snake.update_loop(False)
        #print(snake.direction)
        #print("updated")
        #time.sleep(0.01)

        obs = (snake.snake[0][0] - snake.apple_pos[0], snake.snake[0][1] - snake.apple_pos[1])
        # print(obs)
        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)
        # Take the action!
        set_direction(action)
        if snake.lost:
            reward = -LOSE_PENALTY
        elif snake.score == last_score + 1:
            reward = FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * snake.score)
            i = 0
        else:
            reward = -MOVE_PENALTY
        ## NOW WE KNOW THE REWARD, LET'S CALC YO
        # first we need to obs immediately after the move.
        new_obs = (snake.snake[0][0] - snake.apple_pos[0], snake.snake[0][1] - snake.apple_pos[1])
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        if reward == FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * snake.score):
            new_q = FOOD_BASE_REWARD + (FOOD_BONUS_REWARD * snake.score)
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q

        episode_reward += reward
        #if reward == FOOD_REWARD or reward == -LOSE_PENALTY:
        #    break
        episode_score = snake.score
        i += 1

            #if snake.score > last_score:
            #    print("score: " + str(snake.score))

            # print(episode_reward)

    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

    snake.update_loop(False)
    EPISODE += 1

    score_visual = "I" * last_score
    print("Episode: " + str(EPISODE) + ", \treward: " + str(episode_reward)+ ", \tscore: " + str(episode_score) + "\t" + score_visual)



moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)

