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
        self.data = ["50", "0.5", "15", "50", "1", "15", "3"]
        self.preys_rect = []
        self.predators_rect = []
        self.right_panel_state = True
        self.zoom = 1
        self.buttons_position = {"cancel_selected" : (0, 0)}
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
        self.m = 0
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
        self.vel = 0
        self.angle = rotation_vel
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.rect = pygame.Rect(self.x, self.y, self.img.get_size()[0], self.img.get_size()[1])
        self.health = 100
        self.name = ""
    dt = 0

    def draw(self, screen, position):
        blit_rotate_center(screen, self.img, (self.x - position.x, self.y - position.y), self.angle)

    def scale(self, percent):
        self.img = pygame.transform.scale_by(self.img, percent)

    def moveUp(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        if 0 <= self.x <= Init.cage[0] - 10 and 0 <= self.y <= Init.cage[1] - 10:
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical * Animal.dt
            self.x -= horizontal * Animal.dt
        else:
            if self.x <= 0:
                self.x += 1
            if self.x >= Init.cage[0] - 10:
                self.x -= 1

            if self.y <= 0:
                self.y += 1
            if self.y >= Init.cage[1] - 10:
                self.y -= 1

        self.rect = pygame.Rect(self.x, self.y, self.img.get_size()[0], self.img.get_size()[1])


    def slowObject(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def update(self):
        random = int(uniform(0, 3))
        if random == 1:
            self.angle += 10
        elif random == 2:
            self.angle -= 10
        self.moveUp()


class Prey(Animal):
    IMG = scale_image(pygame.image.load('images/green_object_FILL.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (350, 350)

    def eat(self, predators, init):
        index = pygame.Rect.collidelist(self.rect, init.predators_rect)
        if index != -1:
            predators[index].health -= 20
            if predators[index].health == 0:
                if predators[index] == init.selected[1]:
                    init.selected = False, None
                predators.pop(index)
                init.predators_rect.pop(index)
        return predators


class Predator(Animal):
    IMG = scale_image(pygame.image.load('images/red_object_FILL.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (0, 0)
    def eat(self, preys, init):
        index = pygame.Rect.collidelist(self.rect, init.preys_rect)
        if index != -1:
            preys[index].health -= 50
            self.angle += 180
            self.move()
            self.vel = 0
            self.angle -= 180
            if preys[index].health == 0:
                if preys[index] == init.selected[1]:
                    init.selected = False, None
                preys.pop(index)
                init.preys_rect.pop(index)
        return preys


