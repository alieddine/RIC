import sys

import pygame
import random
import math
from Class import Init

from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))



running = True
surface= pygame.Surface((20,50))
surface.fill((255, 255, 255))
box_x = 200
box_y = 200
speed = 5
init = Init()

clock = pygame.time.Clock()
graph_list = []
image = pygame.image.load("images/background.png")
obj = Rect(5, 5, 20, 20)
while running:
    print(obj.left, obj.top, obj.right, obj.bottom)
    init.clock.tick(60)
    screen.fill((50, 50, 50))
    screen.blit(image, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), obj)
    fps_text = init.font.render(f'FPS : {round(init.clock.get_fps())}', True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    graph_random = random.randint(0, 196)
    graph_list.append([(400, 200), (400, 200 - graph_random)])

    pygame.draw.rect(screen, (255, 255, 255), (48, 48, 404, 204), 2, 2)
    graph_background = pygame.Surface((400, 200))
    graph_background.set_alpha(128)
    graph_background.fill((0, 8, 0, 20))
    for element in graph_list:
        pygame.draw.line(graph_background, (180, 0, 0), element[0], element[1], 2)
        element[0] = element[0][0] - 2, element[0][1]
        element[1] = element[1][0] - 2, element[1][1]
    if graph_list[0][0][0] == 0:
        graph_list.pop(0)

    screen.blit(graph_background, (50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()




    pygame.display.flip()

pygame.quit()