import numpy as np
from time import sleep
import random

def debug_print(obj, data):
    if obj.debug_training:
        print(data)

class Perceptron:
    def __init__(self, weights, fn, threshold, a = None, b = None, bias = None, name=None, desired_output=[-0.5,0.5], debug_training=True):
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
        self.bias = bias
        self.last_inputs = None
        self.last_v = None
        self.last_weights = None
        self.last_result = None
        self.last_sigmaj = None
        self.name = name
        self.desired_output = desired_output
        self.debug_training = debug_training

    def _input_preparing(self, weights, inputs, bias):
        if len(weights) != len(inputs):
            debug_print(self, [weights, inputs])
            raise Exception("Invalid input len")

        debug_print(self, [f'in => {inputs[0]}', f' w -> {weights[0]}'])
        input_parsed = [inputs[i] * weights[i] for i in range(0, len(inputs))]
        input_sum_with_bias = np.sum(input_parsed) + bias if bias != None else 0

        return input_sum_with_bias

    def _degree_activation(self, threshold, weights, prepared_input):
        if prepared_input >= threshold:
            return self.desired_output[1]

        return self.desired_output[0]

    def _sigmoid_fn(x):
        return 1 / (1 + np.power(np.e, -1 * x))

    def _sigmoid_activation(self, threshold, weights, prepared_input):
        result = Perceptron._sigmoid_fn(prepared_input)

        if result > threshold:
            return self.desired_output[1]
        
        return self.desired_output[0]

    def _deriv_sigmoid_fn(prepared_input):
        return Perceptron._sigmoid_fn(prepared_input) * (1 - Perceptron._sigmoid_fn(prepared_input))

    def _deriv_sigmoid_fn(self, alpha = 1):
        return alpha * self.last_result * (1 - self.last_result)


    def _linear_activation(self, threshold, weights, prepared_input):
        result = self.a * prepared_input + self.b

        if result > threshold:
            return self.desired_output[1]
        
        return self.desired_output[0]

    def set_weights(self, weights):
        self.last_weights = self.weights
        self.weights = np.copy(weights)

    def get_weights(self):
        return self.weights, self.last_weights

    def process(self, inputs):
        debug_print(self, f'Processing - {self.name}:')
        self.last_v = self._input_preparing(self.weights, inputs, self.bias)
        result = self.activationFn(self, self.threshold, self.weights, self.last_v)
        self.last_inputs = inputs
        self.last_result = result
        debug_print(self, f'Result -> {inputs} - {self.last_result}')
        return result

    def apply_weights_correction(self, learning_fee, isFromOutputLayer = False, expected_result = None, next_neuron_sigmas = None, next_neuron_connected_weights = None):
        debug_print(self, f'Correcting! - {self.name}:')
        self.last_weights = np.copy(self.weights)
        sigmaj = self.calculate_sigma(isFromOutputLayer, expected_result, next_neuron_sigmas, next_neuron_connected_weights)
        debug_print(self, [sigmaj, self.bias])
        self.bias -= Perceptron.calculate_error_correction(learning_fee, sigmaj, 1)
        for i in range(0, len(self.weights)):
            corr = Perceptron.calculate_error_correction(learning_fee, sigmaj, self.last_inputs[i])
            debug_print(self, f'Adjusting weight {i} -> {corr}')
            self.weights[i] -= corr
        

    def calculate_sigma(self, isFromOutputLayer = False, expected_result = None, next_neuron_sigmas = None, next_neuron_connected_weights = None):
        if isFromOutputLayer:
            err = expected_result - self.last_result
            debug_print(self, f'Calculating sigmaj -> {err} - {self._deriv_sigmoid_fn()}')
            # self.last_sigmaj = Perceptron._deriv_sigmoid_fn(self.last_v) * err
            self.last_sigmaj = self._deriv_sigmoid_fn() * err
            return self.last_sigmaj
        
        # phi_l = Perceptron._deriv_sigmoid_fn(self.last_v)
        phi_l = self._deriv_sigmoid_fn()
        wmul = [next_neuron_sigmas[i] * next_neuron_connected_weights[i] for i in range(len(next_neuron_sigmas))]
        wsum = np.sum(wmul)
        self.last_sigmaj = phi_l * wsum
        return self.last_sigmaj

    def calculate_error_correction(learning_fee, sigmaj, input):
        return learning_fee * sigmaj * input

    def forward(self, inputs):
        pass

    def backward(self, next_neuron_sigma):
        pass

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

class PercyNetwork:
    def __init__(self, neuron_layers, weights, learning_fee, debug_training=True):
        self.layers = neuron_layers
        self.weights = weights
        self.learning_fee = learning_fee
        self.epoch_index = 1
        self.train_epochs_limit = 200
        self.train_epochs_interval = 1000 #ms
        self.train_zero_err_expectation = 5
        self.debug_training = debug_training

        for layer in neuron_layers:
            for neuron in layer:
                neuron.debug_training = debug_training

    def set_training_settings(self, epochs_limit, epochs_interval, zero_err_expectation):
        self.train_epochs_limit = epochs_limit
        self.train_epochs_interval = epochs_interval
        self.train_zero_err_expectation = zero_err_expectation

    def get_neuron(self, layer, index) -> Perceptron:
        return self.layers[layer][index]

    def forward(self, inputs):
        forward_weight_map = []
        output_map = [inputs]

        for layer in range(0, len(self.layers)):
            layer_out = []
            layer_weight_map = []

            for neuron in range(0, len(self.layers[layer])):
                target_neuron = self.get_neuron(layer, neuron)
                out = target_neuron.process(output_map[layer])

                layer_out.append(out)
                layer_weight_map.append(target_neuron.weights)

            output_map.append(layer_out)
            forward_weight_map.append(layer_weight_map)
        
        self.forward_weight_map = forward_weight_map
        self.forward_output_map = output_map

        return output_map[-1][0]

    def backward(self, expected_result):
        backward_sigma_map = []

        for layer in range(len(self.layers) - 1, -1, -1):
            layer_out = []
            layer_sigma_map = []
            isOutputLayer = True if layer == (len(self.layers) - 1) else False

            for neuron in range(0, len(self.layers[layer])):
                target_neuron = self.get_neuron(layer, neuron)

                if isOutputLayer:
                    target_neuron.apply_weights_correction(self.learning_fee, 
                        isFromOutputLayer=isOutputLayer, expected_result=expected_result)
                    # err = expected_outs[neuron] - obtained_outs[neuron]
                    # v = target_neuron.last_v()
                    # phi = target_neuron.deriv_actv(v)
                    # sigma = err * phi
                else:
                    nextNeuronSigmas = []
                    nextNeuronConnectedWeights = []
                    for next_neuron_index in range(len(self.layers[layer + 1])):
                        next_neuron = self.get_neuron(layer + 1, next_neuron_index)
                        nextNeuronSigmas.append(next_neuron.last_sigmaj)
                        nextNeuronConnectedWeights.append(next_neuron.last_weights[neuron])

                    target_neuron.apply_weights_correction(self.learning_fee, 
                        isFromOutputLayer=isOutputLayer, next_neuron_sigmas=nextNeuronSigmas, 
                        next_neuron_connected_weights=nextNeuronConnectedWeights)

            #     layer_sigma_map.append(sigma)
            #     # layer_weight_map.append(target_neuron.weights)

            # backward_sigma_map.append(layer_sigma_map)
            # layer_sigma_map.append(layer_sigma_map)
    
    #One epoch is categorized as the complete usage of the input dataset within the network
    def run_epoch(self, input_dataset):
        errors = []
        for batch in input_dataset:
            expected_out = batch[-1]
            net_output = self.forward(batch[:-1])
            current_err = expected_out - net_output
            errors.append(current_err)

            self.backward(expected_out)
            debug_print(self, f'Running epoch #{self.epoch_index} - err: {current_err}')
        
        self.epoch_index += 1
        return errors

    def train(self, input_dataset):
        run_training = True
        self.epoch_index = 0
        zero_err_cnt = 0
        while run_training and (self.epoch_index <= self.train_epochs_limit):
            current_errors = self.run_epoch(input_dataset)

            err_sum = np.sum(current_errors)
            if err_sum == 0:
                zero_err_cnt += 1
            else:
                zero_err_cnt = 0

            if zero_err_cnt >= self.train_zero_err_expectation:
                run_training = False
                debug_print(self, 'Zero error expectation reached! The perfection was achieved! - Finishing training...')
                return True

            sleep(self.train_epochs_interval / 1000)
        
        debug_print(self, f'Training finished - Executed epochs: {self.epoch_index} - Zero-error counter: {zero_err_cnt}')
        return False

    def predict(self, single_input):
        return self.forward(single_input)