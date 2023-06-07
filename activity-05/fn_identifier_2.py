import numpy as np
from time import sleep
import random
from perceptron import *

neuron_qtt = 6
learning_fee = 0.3
data = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [0, 0, 0]
]

weights = [[random.uniform(-0.5, 0.5) for i in range(0, len(data[0]) - 1 + (1 if j > 2 and j < 5 else 0))] for j in range(0, neuron_qtt)]

print(weights)
# percy = Perceptron(weights[0], 'linear', 0.6, 0.2, 0.8)
# percy2 = Perceptron(weights[1], 'linear', 0.8, 0.4, 0.55)
# percy3 = Perceptron(weights[2], 'linear', 0.95, 0.2, 0.3)

percy = Perceptron(weights[0], 'sigmoid', 0.95)
percy2 = Perceptron(weights[1], 'sigmoid', 0.95)
percy3 = Perceptron(weights[2], 'sigmoid', 0.95)
percy4 = Perceptron(weights[3], 'sigmoid', 0.95)
percy5 = Perceptron(weights[4], 'sigmoid', 0.95)
percy6 = Perceptron(weights[5], 'sigmoid', 0.95)


nnet = [
    [percy, percy2, percy3],
    [percy4, percy5],
    [percy6]
]

idx = 0
good_answers = 0
epoch_counter = 0

_run = True
try:
    while _run:
        result = epoch_n(epoch_counter, nnet, data[idx], weights, learning_fee)
        idx += 1
        epoch_counter += 1

        if result == True and good_answers >= len(data):
            _run = False
            print("Training ended...")
            break

        if result == True:
            good_answers += 1 
        else:
            good_answers = 0

        if len(data) == idx:
            idx = 0
        
        sleep(0.2)

except KeyboardInterrupt:
    print('Percy was killed...')
    _run = False