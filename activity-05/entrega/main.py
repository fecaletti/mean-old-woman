import numpy as np
from time import sleep
import random
from perceptron import *


def encode_binary_dataset(dataset):
    encoded_dataset = []
    for row in dataset:
        encoded_dataset.append([0.5 if i == 1 else -0.5 for i in row])
    return encoded_dataset

neuron_qtt = 3
learning_fee = 0.15
data = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
    [0, 0, 0]
]

# weights = [[random.uniform(-0.5, 0.5) for i in range(0, len(data[0]) - 1 + (1 if j > 2 and j < 5 else 0))] for j in range(0, neuron_qtt)]
weights = [[random.uniform(-0.5, 0.5) for i in range(0, len(data[0]) - 1)] for j in range(0, neuron_qtt)]

print(weights)

percy = Perceptron(weights[0], 'sigmoid', 0.75, bias=0.5, name='first')
percy2 = Perceptron(weights[1], 'sigmoid', 0.85, bias=0.5, name='sec')
percy3 = Perceptron(weights[2], 'sigmoid', 0.95, bias=0.5, name='third')
# percy4 = Perceptron(weights[3], 'sigmoid', 0.95, bias=0.5)
# percy5 = Perceptron(weights[4], 'sigmoid', 0.95, bias=0.5)
# percy6 = Perceptron(weights[5], 'sigmoid', 0.95, bias=0.5)

nnet = [
    # [percy, percy2, percy3],
    [percy, percy2],
    [percy3]
]

idx = 0
good_answers = 0
epoch_counter = 0

_run = True
_run_training = True
network = PercyNetwork(nnet, weights, learning_fee)
try:
    while _run:
        train_result = False
        if _run_training:
            encoded_dataset = encode_binary_dataset(data)
            network.set_training_settings(100, 100, 10)
            train_result = network.train(encoded_dataset)
            _run_training = False

        if not train_result:
            _run = False
            break

        print(f'The training was successful! What do you want to do now?')
        command = (input('Predict result [P] | Quit [Q]: ')).upper()

        if command == 'T':
            _run_training = True
        if command == 'P':
            data = input('Type your input, in the format in1,in2: ')
            parsed = data.split(',')
            encoded_data = [0.5 if d == '1' else -0.5 for d in parsed]
            result = network.predict(encoded_data)
            print(f'Obtained result -> {1 if result == 0.5 else 0}')
        if command == 'Q':
            print('Bye!')
            _run = False

except KeyboardInterrupt:
    print('Percy was killed...')
    _run = False