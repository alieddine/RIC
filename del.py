import math
import pickle

import numpy as np

from genitic import fitness_predator


class NN:
    def __init__(self, input_number=18, neuron_number=2):
        self.weight = 0.1 * np.random.randn(input_number, neuron_number)
        self.bias = 0.1 * np.random.randn(neuron_number)

    def forward_pass(self, input_number):
        # return tan_h(np.dot(input_number, self.weight) + self.bias)
        return tuple(map(tan_h, np.dot(input_number, self.weight) + self.bias))


# tanh
def tan_h(output):
    return math.tanh(output)


input = [0 for _ in range(18)]
obj = NN()


pickle_in_predators = open("data_predators.pickle", "rb")
predators = pickle.load(pickle_in_predators)

p1 = fitness_predator(predators)
print(len(predators))