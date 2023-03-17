import math
import random
import threading

from testFUNCTION import *
import pygame
import sys
import numpy as np

class Animal:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def moveUp(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        print(self.x, self.y)
        if 0 <= self.x <= 1275 and 0 <= self.y <= 675:
            radians = math.radians(self.angle)
            vertical = math.cos(radians) * self.vel
            horizontal = math.sin(radians) * self.vel

            self.y -= vertical
            self.x -= horizontal
        else:
            if self.x <= 0:
                self.x += 1
            if self.x >= 1275:
                self.x -= 1

            if self.y <= 0:
                self.y += 1
            if self.y >= 675:
                self.y -= 1
    def slowObject(self):
        self.vel = max(self.vel - self.acceleration / 0.6, 0)
        self.move()

class Prey(Animal):
    IMG = scale_image(pygame.image.load('images/green_object.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (0, 350)
class Predator(Animal):
    IMG = scale_image(pygame.image.load('images/red_object.png'), 0.2)
    IMG = pygame.transform.rotate(IMG, 90)
    START_POS = (350, 350)

def main(x_y):
    pygame.init()
    screen = pygame.display.set_mode((1300, 700))
    background_image = pygame.image.load('images/background.png')
    background_image = pygame.transform.scale(background_image, (1300, 700))
    predator = pygame.image.load('images/red_object.png')
    predator = pygame.transform.scale(predator, (25, 25))
    # prey = pygame.image.load('green_object.png')
    # prey = pygame.transform.scale(prey, (30, 25))
    clock = pygame.time.Clock()
    i = 0
    j = 0
    x = 70
    y = 350
    pause = False
    prey2 = Prey(6, 5).START_POS = x_y


    while True:
        moving = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_p:
                    pause = not pause
        keys = pygame.key.get_pressed()
        '''
        if keys[pygame.K_a]:
            prey1.rotate(left=True)
        if keys[pygame.K_d]:
            prey1.rotate(right=True)
        if keys[pygame.K_w]:
            moving = True
            prey1.moveUp()

        if not moving:
            prey1.slowObject()
        '''
        if pause:
            continue
        ran = random.randrange(3)
        if ran == 1:
            prey2.rotate(left=True)
        elif ran ==2:
            prey2.rotate(right=True)

        prey2.moveUp()
        screen.fill((120, 120, 120))

        screen.blit(background_image, (0, 0))
        # prey1.draw(screen)
        screen.blit(predator, (i, 350))
        # i = i + 1
        clock.tick(30)
        pygame.display.update()


if __name__ == '__main__':

    x_y = np.random.randint(low=0, high=500, size=(2, 2))
    threads = []
    for element in x_y:
        thread = threading.Thread(target=main, args=(element,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()