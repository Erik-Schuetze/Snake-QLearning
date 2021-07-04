import ast
import json
from sklearn.utils import shuffle
import tensorflow as tf
import numpy as np

import os, sys
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

checkpoint_path = "cp3.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)


cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# load dataset
file = open("data.txt", "r")

lines = file.readlines()
#snake_dataset = np.array([lines])

batchsize = len(lines) - 500
inputs = []
targets = []
last_gamestate = []
batchcount = 0

for line in lines:
    if batchcount == 0:
        data_array = ast.literal_eval(line)
        last_gamestate = data_array[0]
    elif batchcount > 0:
        data_array = ast.literal_eval(line)
        #print(data_array)
        gamestate, direction = data_array[0], data_array[1]

        for i in range(len(last_gamestate)):
            gamestate.append(last_gamestate[i])

        data_array = ast.literal_eval(line)
        last_gamestate = data_array[0]

        inputs.append(gamestate)
        targets.append(direction)

        if batchcount == batchsize:
            train_X = np.array(inputs, dtype='float32')
            train_Y = np.array(targets, dtype='float32')
            #yield (X, y)
            inputs = []
            targets = []
            #batchcount = 0
        if batchcount > batchsize and batchcount == len(lines) - 3:
            test_X = np.array(inputs, dtype='float32')
            test_Y = np.array(targets, dtype='float32')
    batchcount += 1

        # yield (X, y)
        #inputs = []
        #targets = []
        #batchcount = 0
    #if batchcount == len(data_array) - 2:

    #snake_dataset.append(line)
print(train_X.shape)
print(train_Y.shape)
print(test_X.shape)
print(test_Y.shape)


# labels
class_names = ['up', 'right', 'down', 'left']

# scale values to map from 0 - 1
train_X = train_X / 3.0
test_X = test_X / 3.0

train_X, train_Y = shuffle(train_X, train_Y)

print(train_X.shape)

# build model with layers
#model = tf.keras.Sequential([
#    tf.keras.layers.Flatten(input_shape=(28, 28)),  # transforms 28x28 array into 784 "neuron" array
#    tf.keras.layers.Dense(100, activation='tanh'),  # dense - fully connected
#    tf.keras.layers.Dense(10)                       # output layer
#])


model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(20, 10)),
        tf.keras.layers.Dense(100, activation='tanh'),
        tf.keras.layers.Dense(50, activation='relu'),
        tf.keras.layers.Dense(4)
    ])


model.compile(optimizer='adam',  # how model gets updated based on data and loss f
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # loss f
              metrics=['accuracy'])  # used to monitor traing and testing steps

# train model on train data set
# added callback = checkpoint
model.fit(train_X, train_Y, epochs=10, callbacks=[cp_callback])

# test on dataset
test_loss, test_acc = model.evaluate(test_X, test_Y, verbose=2)
print('\nTest accuracy:', test_acc)


# softmax layer converts logits to probabilities
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

# build array with all predictions
predictions = probability_model.predict(test_X)

# ausgabe der ersten prediction werte von 0 - 9
#print('\nPrediction Werte:', predictions[0])

# print best predictions for x images
for i in range(0, 3):
    print('\nBest Guess:', np.argmax(predictions[i]))
    print('Correct Guess',test_Y[i])


# take and print random test image shape
img = test_X[100]

# Add the image to a batch where it's the only member.
# Keras uses batches to make predictions on a collection of things at once
img = (np.expand_dims(img,0))

#
predictions_single = probability_model.predict(img)
print('Prediction of batch:', predictions_single)
print('Best guess of batch:', np.argmax(predictions_single[0]))
print('Correct Guess',test_Y[100])






