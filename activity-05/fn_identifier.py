import numpy as np
from time import sleep
import random
from perceptron import *


data = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
]
weights = [random.uniform(-0.5, 0.5) for i in range(0, len(data[0]) - 1)]
learning_fee = 1.5

percy = Perceptron(weights, 'linear', 0.95, 0.2, 0.3)
idx = 0
good_answers = 0
epoch_counter = 0

_run = True
try:
    while _run:
        result = epoch(epoch_counter, percy, data[idx], weights, learning_fee)
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
        
        sleep(1)

except KeyboardInterrupt:
    print('Percy was killed...')
    _run = False