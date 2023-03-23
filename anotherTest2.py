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
i = 0
angle_1 = - 10
angle_2 = 0
angle_3 = 10
while running:
    # print(obj.left, obj.top, obj.right, obj.bottom)
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
    rect = Rect(500, 400,50,50)

    radians_1 = math.radians(angle_1-90)
    radians_2 = math.radians(angle_2-90)
    radians_3 = math.radians(angle_3-90)
    vertical_1 = math.cos(radians_1) * 900
    vertical_2 = math.cos(radians_2) * 900
    vertical_3 = math.cos(radians_3) * 900
    horizontal_1 = math.sin(radians_1) * 900
    horizontal_2 = math.sin(radians_2) * 900
    horizontal_3 = math.sin(radians_3) * 900
    pygame.draw.rect(screen, (255,255,255), rect)

    line_1 = (400, 500), (400 + vertical_1, 500 + horizontal_1)
    line_2 = (400, 500), (400 + vertical_2, 500 + horizontal_2)
    line_3 = (400, 500), (400 + vertical_3, 500 + horizontal_3)
    coordinates_1 = rect.clipline(line_1)
    coordinates_2 = rect.clipline(line_2)
    coordinates_3 = rect.clipline(line_3)
    if coordinates_1:
        pygame.draw.line(screen, (255, 0, 0), (400, 500), coordinates_1[0] , 2)
    else:
        pygame.draw.line(screen, (255, 255, 255), (400, 500), (400+ vertical_1, 500+horizontal_1), 2)
    if coordinates_2:
        pygame.draw.line(screen, (255, 0, 0), (400, 500), coordinates_2[0] , 2)
    else:
        pygame.draw.line(screen, (255, 255, 255), (400, 500), (400+ vertical_2, 500+horizontal_2), 2)
    if coordinates_3:
        pygame.draw.line(screen, (255, 0, 0), (400, 500), coordinates_3[0] , 2)
    else:
        pygame.draw.line(screen, (255, 255, 255), (400, 500), (400+ vertical_3, 500+horizontal_3), 2)


    i += 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_LEFT:
                angle_1 -= 5
                angle_2 -= 5
                angle_3 -= 5
            else:
                angle_1 += 5
                angle_2 += 5
                angle_3 += 5




    pygame.display.flip()

pygame.quit()