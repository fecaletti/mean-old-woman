import numpy as np
from time import sleep
import random

class Perceptron:
    def __init__(self, weights, fn, threshold, a = None, b = None):
        self.weights = np.copy(weights)

        if fn == 'degree':
            self.activationFn = Perceptron._degree_activation
        if fn == 'sigmoid':
            self.activationFn = Perceptron._sigmoid_activation
        if fn == 'linear':
            self.activationFn = Perceptron._linear_activation

        self.threshold = threshold
        self.a = a
        self.b = b

    def _input_preparing(weights, inputs):
        if len(weights) != len(inputs):
            print(weights, inputs)
            raise Exception("Invalid input len")

        input_parsed = [inputs[i] * weights[i] for i in range(0, len(inputs))]
        input_sum = np.sum(input_parsed)

        return input_sum

    def _degree_activation(self, threshold, weights, prepared_input):
        if prepared_input >= threshold:
            return True

        return False

    def _sigmoid_activation(self, threshold, weights, prepared_input):
        result = 1 / (1 + np.power(np.e, -1 * prepared_input))

        if result > threshold:
            return True
        
        return False

    def _linear_activation(self, threshold, weights, prepared_input):
        result = self.a * prepared_input + self.b

        if result > threshold:
            return True
        
        return False

    def set_weights(self, weights):
        self.weights = np.copy(weights)

    def process(self, inputs):
        prepared_input = Perceptron._input_preparing(self.weights, inputs)
        return self.activationFn(self, self.threshold, self.weights, prepared_input)

def epoch(epoch_index, neuron, batch, weights, learning_fee):
    inputs = batch[:-1]
    result = neuron.process(inputs)
    error = batch[-1] - result
    print(f'Epoch #{epoch_index} - expected: {batch[2]} - obtained: {result} - error: {error}')

    if error != 0:
        for i in range(0, len(weights)):
            weights[i] += (learning_fee * inputs[i] * error)

        neuron.set_weights(weights)
        return False
    
    print(f'The perfection was achieved! weights: {weights}')
    return True

def epoch_n(epoch_index, neuron_layers, batch, weights, learning_fee):
    inputs = batch[:-1]
    last_layer_out = inputs
    layer_idx = 0
    output_map = []
    input_map = [inputs]

    for layer in neuron_layers:
        new_layer_out = []
        for neuron in layer:
            new_layer_out.append(neuron.process(last_layer_out))
        output_map.append(np.copy(new_layer_out))
        input_map.append(np.copy(new_layer_out))
        last_layer_out = np.copy(new_layer_out)

    result = last_layer_out[0]
    error = batch[-1] - result
    print(f'Epoch #{epoch_index} - expected: {batch[2]} - obtained: {result} - error: {error}')

    if error != 0:
        neuron_cnt = 0
        for l in range(0, len(neuron_layers)):
            for n in range(0, len(neuron_layers[l])):
                for i in range(0, len(weights[neuron_cnt])):
                    weights[neuron_cnt][i] += (learning_fee * input_map[l][i] * error)
                neuron_layers[l][n].set_weights(weights[neuron_cnt])
                neuron_cnt += 1

        return False
    
    print(f'The perfection was achieved! weights: {weights}')
    return True