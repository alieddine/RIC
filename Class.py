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
        self.data = None



class Position:
    def __init__(self):
        self.x = 0
        self.y = 0


class Animal:
    cage = 0, 0  # static

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.angle = rotation_vel
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

        self.health = 100
    dt = 0

    def draw(self, screen, position):
        blit_rotate_center(screen, self.img, (self.x - position.x, self.y - position.y), self.angle)

    def scale(self, percent):
        self.img = pygame.transform.scale_by(self.img, percent)

    def moveUp(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):

        if 0 <= self.x <= Animal.cage[0] - 10 and 0 <= self.y <= Animal.cage[1] - 10:
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical * Animal.dt
            self.x -= horizontal * Animal.dt
        else:
            if self.x <= 0:
                self.x += 1
            if self.x >= Animal.cage[0] - 10:
                self.x -= 1

            if self.y <= 0:
                self.y += 1
            if self.y >= Animal.cage[1] - 10:
                self.y -= 1

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
    START_POS = (0, 350)

    def eat(self, predators):
        for predator in predators:
            if predator.x <= self.x <= predator.x + predator.IMG.get_size()[0] and predator.y <= self.y <= predator.y + \
                    predator.IMG.get_size()[
                        1] \
                    or predator.x <= self.x + predator.IMG.get_size()[0] <= predator.x + predator.IMG.get_size()[
                0] and predator.y <= self.y <= predator.y + predator.IMG.get_size()[1] \
                    or predator.x <= self.x <= predator.x + predator.IMG.get_size()[0] and predator.y <= self.y + \
                    predator.IMG.get_size()[
                        1] <= predator.y + predator.IMG.get_size()[1] \
                    or predator.x <= self.x + predator.IMG.get_size()[0] <= predator.x + predator.IMG.get_size()[
                0] and predator.y <= self.y + predator.IMG.get_size()[1] <= predator.y + predator.IMG.get_size()[1]:

                predator.health -= 20
                if predator.health == 0:
                    predators.remove(predator)
            # if self.IMG.get_rect().collidepoint(prey.x, prey.y):
            #     preys.remove(prey)

        return predators


class Predator(Animal):
    IMG = scale_image(pygame.image.load('images/red_object_FILL.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (350, 350)

    def eat(self, preys):
        for prey in preys:
            if prey.x <= self.x <= prey.x + prey.IMG.get_size()[0] and prey.y <= self.y <= prey.y + prey.IMG.get_size()[
                1] \
                    or prey.x <= self.x + prey.IMG.get_size()[0] <= prey.x + prey.IMG.get_size()[
                0] and prey.y <= self.y <= prey.y + prey.IMG.get_size()[1] \
                    or prey.x <= self.x <= prey.x + prey.IMG.get_size()[0] and prey.y <= self.y + prey.IMG.get_size()[
                1] <= prey.y + prey.IMG.get_size()[1] \
                    or prey.x <= self.x + prey.IMG.get_size()[0] <= prey.x + prey.IMG.get_size()[
                0] and prey.y <= self.y + prey.IMG.get_size()[1] <= prey.y + prey.IMG.get_size()[1]:

                prey.health -= 50
                self.angle += 180
                self.move()
                self.vel = 0
                self.angle -= 180

                if prey.health == 0:
                    preys.remove(prey)
            # if self.IMG.get_rect().collidepoint(prey.x, prey.y):
            #     preys.remove(prey)

        return preys
