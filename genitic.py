import pickle
from random import random, shuffle, choice, randrange

import numpy as np


def genitic_fun():
    pickle_in_preys = open("data_preys.pickle", "rb")
    preys = pickle.load(pickle_in_preys)

    pickle_in_predators = open("data_predators.pickle", "rb")
    predators = pickle.load(pickle_in_predators)
    p1 = fitness_predator(predators)
    p1 = selction_predator(p1)
    best1 = p1[:20]
    p1 = croisment(p1)
    p1 = mutaion(p1)
    p1 = best1 + p1
    p2 = fitness_prey(preys)
    p2 = selction_prey(p2)
    best2 = p2[:40]
    p2 = croisment(p2)
    p2 = mutaion(p2)
    p2 = best2 + p2

    pickle_out = open("genitic_data_preys.pickle", "wb")
    pickle.dump(p2, pickle_out)
    pickle_out.close()
    pickle_out_2 = open("genitic_data_predators.pickle", "wb")
    pickle.dump(p1, pickle_out_2)
    pickle_out_2.close()


"""0 : wieghts , 
   1 : baiss , 
   2 : kills ,
   3 : age , 
"""


def fitness_predator(array):
    max_kill = max(element[2] for element in array)
    if max_kill == 0: max_kill = 1
    max_age = max(element[3] for element in array)
    for element in array:
        evalute = element[2] * 90 / max_kill
        evalute += element[3] * 20 / max_age
        element.append(evalute)
    return array

def fitness_prey(array):
    max_age = max(element[2] for element in array)
    for element in array:
        evalute = element[2] * 100 / max_age
        element.append(evalute)
    return array


def selction_predator(array):

    array = sorted(array, key=lambda x: x[4], reverse=True)
    array = array[:len(array) // 5]
    return array


def selction_prey(array):

    array = sorted(array, key=lambda x: x[3], reverse=True)
    array = array[:len(array) // 2]
    return array


def croisment(array):
    shuffle(array)
    half_index = len(array) // 2

    array_1 = array[:half_index]
    array_2 = array[half_index:]
    size = min(len(array_1), len(array_2))
    # half_index = len(array_1[0][0]) // 2
    half_index = 9
    for i in range(size):
        new_array_1 = np.concatenate((array_2[i][0][half_index:], array_1[i][0][:half_index]))
        new_array_2 = np.concatenate((array_1[i][0][half_index:], array_2[i][0][:half_index]))

        # new_bais_1 = np.concatenate((array_2[i][1][0], array_1[i][1][1]))
        # new_bais_2 = np.concatenate((array_1[i][1][0], array_2[i][1][1]))

        array_1[i][0] = new_array_1
        array_2[i][0] = new_array_2
        # array_1[i][1] = new_bais_1
        # array_2[i][1] = new_bais_2
        array_1[i][1][0] = array_2[i][1][0]
        array_1[i][1][1] = array_1[i][1][1]
        array_2[i][1][0] = array_1[i][1][0]
        array_2[i][1][1] = array_2[i][1][1]
    return array_1 + array_2


# def mutaion(array):
#     for j in range(10):
#         index = choice([i for i in range(len(array))])
#         index2 = choice([i for i in range(17)])
#         array[index][0][index2] = np.random.randn(2)
#         index3 = choice([i for i in range(len(array))])
#         array[index3][1] = np.random.randn(2)
#     return array


def mutaion(array):
    wheel = randrange(0, 100)
    if wheel < 50:
        for i in range(2):
            index = choice([i for i in range(len(array))])
            index2 = choice([i for i in range(17)])
            array[index][0][index2] = np.random.randn(2)
            index3 = choice([i for i in range(len(array))])
            array[index3][1] = np.random.randn(2)
    return array


def main():
    pickle_in_preys = open("data_preys.pickle", "rb")
    preys = pickle.load(pickle_in_preys)

    pickle_in_predators = open("data_predators.pickle", "rb")
    predators = pickle.load(pickle_in_predators)

    p1 = fitness_predator(predators)
    p1 = selction_predator(p1)
    best1 = p1[:20]
    p2 = fitness_prey(preys)
    p2 = selction_prey(p2)
    best2 = p2[:20]
    pickle_in_preys = open("best_data_preys.pickle", "wb")
    pickle.dump(best2, pickle_in_preys)
    pickle_in_preys.close()

    pickle_in_predators = open("best_data_predators.pickle", "wb")
    pickle.dump(best1, pickle_in_predators)
    pickle_in_predators.close()


if __name__ == '__main__':
    main()

# p = fitness(predators)
# p = selction(p)
# p = croisment(p)
#
# for i in range(len(p)):
#     print("evalute : ", p[i][0])