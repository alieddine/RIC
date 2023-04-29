from math import exp
import numpy as np


class NN:
    def __init__(self, input_number, neuron_number):
        self.predicted_output = 0
        self.output = 0
        self.error = 0
        self.weight = 0.1 * np.random.randn(input_number, neuron_number)
        self.bias = 0.1 * np.random.randn(neuron_number)
        self.alpha = 1

    def forward_pass(self, input_number):
        self.output = np.dot(input_number, self.weight) + self.bias

    def sigmoid(self, output):
        self.predicted_output = 1 / (1 + exp(- self.alpha * output))

    def calculate_error(self, desired_output):
        self.error = -self.predicted_output + desired_output

    def correct_weights(self, inputs):
        for i in range(len(self.weight)):
            self.weight[i] += self.alpha * self.error * inputs[i]
        self.bias += self.alpha * self.error


def main():
    example_input = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]
    desired_output = [1, 0, 0, 1]

    neuron = NN(len(example_input[0]), 1)
    print(neuron.weight)
    j = 0
    print(neuron.predicted_output)
    # while True:
    #     error = 0
    #
    #     print(f"iteration {j} :")
    #     for i in range(len(example_input)):
    #         neuron.forward_pass(example_input[i])
    #         neuron.sigmoid(neuron.output)
    #         neuron.calculate_error(desired_output[i])
    #         neuron.correct_weights(example_input[i])
    #         print(neuron.predicted_output)
    #         error += abs(neuron.error)
    #     j += 1
    #     print(neuron.weight, neuron.bias)
    #     if error < 0.01:
    #         break
    #
    neuron1 = NN(2, 1)
    neuron1.weight = [[11.11652457], [-11.5373004]]
    neuron1.bias = [-5.69853552]

    neuron2 = NN(2, 1)
    neuron2.weight = [[-11.5356992], [11.1149232]]
    neuron2.bias = [-5.69773553]

    neuron3 = NN(2, 1)
    neuron3.weight = [[11.29941711], [11.30380646]]
    neuron3.bias = [-5.18832913]
    for i in range(4):
        neuron1.forward_pass(example_input[i])
        neuron1.sigmoid(neuron1.output)
        neuron2.forward_pass(example_input[i])
        neuron2.sigmoid(neuron2.output)
        neuron3.forward_pass((neuron1.predicted_output, neuron2.predicted_output))
        neuron3.sigmoid(neuron3.output)
        print(neuron3.predicted_output)

# OR [[11.29941711] [11.30380646]] [-5.18832913]
# A AND NOT B [[ 11.11652457] [-11.5373004 ]] [-5.69853552]
# NOT A AND B [[-11.5356992] [ 11.1149232]] [-5.69773553]

if __name__ == '__main__':
    main()
