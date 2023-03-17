import pygame
import random
import math




pygame.init()
screen = pygame.display.set_mode((800,600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

running = True
surface= pygame.Surface((20,50))
surface.fill((255, 255, 255))
box_x = 200
box_y = 200
speed = 5
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    surface.scroll(10, 10)
    screen.blit(surface, (box_x + speed, box_y + speed))




    pygame.display.flip()

pygame.quit()