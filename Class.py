import numpy as np
import pygame
from testFUNCTION import *
import math
from random import uniform


class Init:
    def __init__(self):
        self.menu = True
        self.font = pygame.font.Font('font/cc-ultimatum-bold.otf', 15)
        self.font3 = pygame.font.Font('font/cc-ultimatum-bold.otf', 50)
        self.font2 = pygame.font.Font('font/cc-ultimatum-bold.otf', 22)
        self.name_text = self.font.render('predator vs prey', True, (255, 255, 255))
        self.clock = pygame.time.Clock()
        self.preys_number = 0
        self.predators_number = 0
        self.display = pygame.display.Info()
        self.exit_btn = pygame.image.load('images/exist_btn.png')
        self.menu_background = None
        self.data = ["200", "0.5", "5", "100", "1", "5", "1.7"]
        self.preys = []
        self.predators = []
        self.zoom = 1
        self.zoom_type = None
        self.pause = False
        self.time = time.time()
        self.saved_preys = []
        self.saved_predators = []

        self.walls = []


        self.prey_original_img = pygame.transform.rotate(scale_image(pygame.image.load("images/green_object_FILL.png"), 0.2), 90)
        self.predator_original_img = pygame.transform.rotate(scale_image(pygame.image.load("images/red_object_FILL.png"), 0.2), 90)
        self.predator1_original_img = pygame.transform.rotate(scale_image(pygame.image.load("images/test_object.png"), 0.2), 90)
        # self.background_original_img = pygame.transform.scale(pygame.image.load("images/background.png"), (self.display.current_w * 0.8, self.display.current_h))
        self.background_original_img = pygame.transform.scale_by(pygame.image.load("images/background.png"), 3)
        self.mouse = (0, 0)
        self.selected = (False, None)
        self.camera_rect = None
        self.show_hide_graph = False
        self.graph_prey_lines = []
        self.prev_time = time.time()
        self.half_seceond_passed = False
        self.max_preys = 0
        self.max_predators = 0
        self.m = 0
        self.m_predator = 0

        self.graph_predator_lines = []

        self.buttons_position = {"side_bar_prey":[None,None,None,None,False],"cancel_selected": (0, 0), "plus_button": (self.display.current_w * 0.82 + self.font2.size(f'Zoom : {round(self.zoom)}')[0],self.display.current_h * 0.1 + 5),"minus_button": (self.display.current_w * 0.84 + self.font2.size(f'Zoom : {round(self.zoom)}')[0],self.display.current_h * 0.1 + 5),"default_button": (self.display.current_w * 0.84 + self.font2.size(f'Zoom : {round(self.zoom)}')[0] + 30, self.display.current_h * 0.1),"show_hide_graph": ((self.display.current_w * 0.81 + self.font2.size("show graph : ")[0] + 5, self.display.current_h * 0.1 + self.font2.size("A")[1] * 2), False),"show_hide_predators_preys_status": ((self.display.current_w * 0.81 +self.font2.size("Preys and Predators :  ")[0],self.display.current_h * 0.1 +self.font2.size("a")[1] * 3), False),"default_button": (self.display.current_w * 0.84 + self.font2.size(f'Zoom : {round(self.zoom)}')[0] + 30, self.display.current_h * 0.1), "up_prey":((self.display.current_w *0.8 + self.display.current_w *0.2*0.05+ self.display.current_w *0.2*0.95*0.02, self.display.current_h * 0.3 +  self.display.current_h * 0.7 * 0.07 +  self.display.current_h * 0.93 *0.02 *0.7), False)}
        self.up_down_prey = 0

        self.width = 0
        self.height = 0
        self.cel_size = 150
        self.cols = 0
        self.rows = 0
        self.buckets = {}
        self.position = 0,0
        self.screen = None
    cage = 0, 0


class background_objects_class:
    def __init__(self):
        self.speed_x = random.uniform(0, 1)
        self.speed_y = random.uniform(0, 1)
        self.direction = 1
        self.angel = random.uniform(0, 360)

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0


class Animal:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 5
        self.angle = rotation_vel
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.rect = pygame.Rect(self.x, self.y, self.img.get_size()[0], self.img.get_size()[1])
        self.health = 100
        self.name = ""
        self.birthday = time.time()
        self.input = [0 for _ in range(18)]
        self.age = 1
        self.kills = 0
        self.nn = None
    dt = 0

    def draw(self, screen, position):
        blit_rotate_center(screen, self.img, (self.x - position.x, self.y - position.y), self.angle)

    def scale(self, percent):
        self.img = pygame.transform.scale_by(self.img, percent)


    def moveUp(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        y = self.y
        x = self.x
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical * Animal.dt
        self.x -= horizontal * Animal.dt
        if not (0 < self.x < Init.cage[0] - self.img.get_size()[0] and 0 < self.y < Init.cage[1] - self.img.get_size()[1]):
            self.x = x
            self.y = y
            if self.x <= 0:
                self.x = 0
            elif self.x >= Init.cage[0] - self.img.get_size()[0]:
                self.x = Init.cage[0] - self.img.get_size()[0]

            if self.y <= 0:
                self.y = 0
            elif self.y >= Init.cage[1] - self.img.get_size()[1]:
                self.y = Init.cage[1] - self.img.get_size()[1]

        self.rect = pygame.Rect(self.x, self.y, self.img.get_size()[0], self.img.get_size()[1])


    def slowObject(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    # def update(self):
    #     random = int(uniform(0, 3))
    #     if random == 1:
    #         self.angle += 10
    #     elif random == 2:
    #         self.angle -= 10
    #     self.moveUp()


class Prey(Animal):
    IMG = scale_image(pygame.image.load('images/green_object_FILL.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (350, 350)



    def eat(self, predators, init):
        index = pygame.Rect.collidelist(self.rect, init.predators)
        if index != -1:
            predators[index].health -= 10
            self.angle += 180
            self.vel = 2
            self.move()
            self.vel = 0
            self.angle -= 180
            if predators[index].health == 0:
                if predators[index] == init.selected[1]:
                    init.selected = False, None
                predators.pop(index)
                init.predators.pop(index)
        return predators

    def update(self, zoom=1):
        if self.age != 1:self.age = round(time.time() - self.birthday, 2)
        else: self.age = 2

        output = self.nn.forward_pass(self.input)
        self.angle += 10 * output[0]
        self.vel = zoom *  0.8 * abs(output[1])
        self.move()

class Predator(Animal):
    IMG = scale_image(pygame.image.load('images/red_object_FILL.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (200,200)
    def eat(self, preys, init):
        index = pygame.Rect.collidelist(self.rect, init.preys)
        if index != -1:
            preys[index].health -= 10
            self.angle += 180
            self.vel = 2
            self.move()
            self.vel = 0
            self.angle -= 180
            if preys[index].health == 0:
                if preys[index] == init.selected[1]:
                    init.selected = False, None
                preys.pop(index)
                if init.up_down_prey - 2 >= 0 :init.up_down_prey -= 2
                init.preys.pop(index)
        return preys

    def update(self, zoom=1):
        if self.age != 1:self.age = round(time.time() - self.birthday, 2)
        else: self.age = 2

        output = self.nn.forward_pass(self.input)
        self.angle += 10 * output[0]
        self.vel = zoom * output[1]
        self.move()


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



def sigmoid(output):
    return 1 / (1 + np.exp(- 1 * output))

