import math
import random
import threading, queue


from testFUNCTION import *
import pygame, time
import sys
import numpy as np
from Class import *


def main():
    pygame.init()
    init = Init()

    screen = pygame.display.set_mode((init.display.current_w, init.display.current_h), pygame.FULLSCREEN)
    prev_time = time.time()
    dt = 0
    TARGET_FPS = 60
    background_image = pygame.image.load('images/background.png')
    background_image = pygame.transform.scale(background_image, (init.display.current_w * 0.8, init.display.current_h))

    pause = False
    predator1 = Prey(500, 5)
    img = scale_image(pygame.image.load("images/test_object.png"), 0.2)
    predator1.img = pygame.transform.rotate(img, 90)

    position = Position()
    scale = False
    zoom = 1
    screen.get_width()
    prey_selected = False
    is_it_selected = False

    camera_borders = {'left': 400, 'right': init.display.current_w * 0.25, 'top': 400, 'bottom': init.display.current_h * 0.25}
    w = init.display.current_w - (camera_borders['left'] + camera_borders['right'])
    h = init.display.current_h - (camera_borders['top'] + camera_borders['bottom'])
    camera_rect = pygame.Rect((camera_borders['left'], camera_borders['top'], w, h))

    while True:

        Animal.cage = background_image.get_size()
        moving = False

        if init.menu:
            menu_panel(screen, init)
            print("lolW")
            preys, predators = set_preys_predators(init)
            prev_time = time.time()
        mouse = pygame.mouse.get_pos()
        now = time.time()
        Animal.dt = (now - prev_time) * TARGET_FPS
        prev_time = now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if init.display.current_w - 30 <= mouse[0] <= init.display.current_w - 20 and 10 <= mouse[1] <= 30:
                    # sys.exit()
                    scale = not scale
                else:
                    new_rect = pygame.draw.rect(screen, (0, 0, 0), (predator1.x - position.x, predator1.y - position.y, predator1.IMG.get_width() * zoom, zoom * predator1.IMG.get_height()), 5, 3)
                    if new_rect.collidepoint(mouse[0], mouse[1]):
                        is_it_selected = True
                        selected = predator1
                        prey_selected = True
                    elif not prey_selected:
                        for prey in preys:
                            new_rect = pygame.draw.rect(screen, (0, 0, 0), (
                            prey.x - position.x, prey.y - position.y, prey.IMG.get_width() * zoom,
                            zoom * prey.IMG.get_height()), 5, 3)
                            if new_rect.collidepoint(mouse[0], mouse[1]):
                                is_it_selected = True
                                selected = prey
                    if not prey_selected:
                        for predator in predators:
                            new_rect = pygame.draw.rect(screen, (0, 0, 0), (
                            predator.x - position.x, predator.y - position.y, predator.IMG.get_width() * zoom,
                            zoom * predator.IMG.get_height()), 5, 3)
                            if new_rect.collidepoint(mouse[0], mouse[1]):
                                is_it_selected = True
                                selected = predator
                    prey_selected = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_p:
                    pause = not pause
        keys = pygame.key.get_pressed()
        if pause:
            continue
        if keys[pygame.K_a]:
            predator1.angle += 10

        if keys[pygame.K_d]:
            predator1.angle -= 10
        if keys[pygame.K_w]:
            moving = True
            predator1.moveUp()
            preys = predator1.eat(preys)

        for predator in predators:
            preys = predator.eat(preys)
        for prey in preys:
            predators = prey.eat(predators)
        if not moving:
            predator1.slowObject()


        screen.fill((50, 50, 50))

        if scale:
            zoom *= 2
            predator1.scale((2, 2))
            predator1.max_vel *= 2
            predator1.acceleration *= 2
            background_image = pygame.transform.scale_by(background_image, (2, 2))
        else:
            predator1.scale(1)
            background_image = pygame.transform.scale_by(background_image, 1)

        predator1.draw(screen, position)
        screen.blit(background_image, (0 - position.x, 0 - position.y))

        # threads = []
        for prey in preys:
            prey.update()
            if scale:
                prey.scale((2, 2))
                prey.max_vel *= 2
                prey.x, prey.y = prey.x * 2, prey.y * 2
            else:
                prey.scale(1)

            prey.draw(screen, position)
        for predator in predators:
            predator.update()
            if scale:
                predator.scale((2, 2))
                predator.max_vel *= 2

                predator.x, predator.y = predator.x * 2, predator.y * 2
            else:
                predator.scale(1)
            predator.draw(screen, position)

        """
        for thread in threads:
            thread.join()
        for prey in preys:
            prey.draw(screen)
        """
        pygame.draw.rect(screen, (255, 255, 255), (0 - position.x, 0 - position.y, Animal.cage[0], Animal.cage[1]), 2,
                         2)

        #  old camera
        # if is_it_selected:
        #     if selected.x - position.x != background_image.get_width() / (4 * zoom):
        #         position.x += selected.x - (position.x + background_image.get_width() / (4 * zoom))
        #     if selected.y - position.y != background_image.get_height() / (4 * zoom):
        #         position.y += selected.y - (position.y + background_image.get_height() / (4 * zoom))
        #     data_panel(screen, selected, Animal.cage)
        #     pygame.draw.rect(screen, (0, 0, 0), (selected.x - position.x, selected.y - position.y, selected.IMG.get_width() * zoom, zoom * selected.IMG.get_height()), 2*zoom, 3)

        if is_it_selected:

            if selected.x < camera_rect.left:
                camera_rect.left = selected.x
            if selected.y < camera_rect.top:
                camera_rect.top = selected.y
            if selected.x + selected.img.get_size()[0] > camera_rect.right:
                camera_rect.right = selected.x + selected.img.get_size()[0]
            if selected.y + selected.img.get_size()[1] > camera_rect.bottom:
                camera_rect.bottom = selected.y + selected.img.get_size()[1]

            position.x = camera_rect.left - camera_borders['left']
            position.y = camera_rect.top - camera_borders['top']
            data_panel(screen, selected, Animal.cage)
            pygame.draw.rect(screen, (0, 0, 0), (
            selected.x - position.x, selected.y - position.y, selected.IMG.get_width() * zoom,
            zoom * selected.IMG.get_height()), 2 * zoom, 3)

        init.clock.tick(500)

        # print(clock.get_fps())
        draw(screen, init)
        pygame.display.update()
        scale = False


if __name__ == '__main__':
    main()
