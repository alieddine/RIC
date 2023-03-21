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
    background_image = pygame.image.load('images/background.png').convert()
    # background_image = pygame.transform.scale(background_image, (init.display.current_w * 0.8, init.display.current_h))
    background_image = pygame.transform.scale_by(background_image, 3).convert()


    pause = False
    predator1 = Predator(30, 5)
    img = scale_image(pygame.image.load("images/test_object.png"), 0.2)
    predator1.img = pygame.transform.rotate(img, 90)

    position = Position()
    zooming_in = False
    zooming_out = False
    zooming_default = False

    init.zoom = 1
    screen.get_width()
    prey_selected = False

    camera_borders = {'left': 400, 'right': init.display.current_w * 0.25, 'top': 400, 'bottom': init.display.current_h * 0.25}
    w = init.display.current_w - (camera_borders['left'] + camera_borders['right'])
    h = init.display.current_h - (camera_borders['top'] + camera_borders['bottom'])
    camera_rect = pygame.Rect((camera_borders['left'], camera_borders['top'], w, h))


    while True:
        init.camera_rect = camera_rect

        moving = False

        if init.menu:
            rest = menu_panel(screen, init)

            if rest:
                prev_time = time.time()
                init.background_original_img = pygame.transform.scale_by(pygame.image.load("images/background.png"), float(init.data[6])).convert()
                background_image = init.background_original_img
                Init.cage = background_image.get_size()
                zooming_default = True
                position.x, position.y = 0, 0
                preys, predators = set_preys_predators(init)
            init.prev_time = time.time()
            init.half_seceond_passed = False
        Init.cage = background_image.get_size()
        mouse = pygame.mouse.get_pos()
        init.mouse = mouse
        now = time.time()
        Animal.dt = (now - prev_time) * TARGET_FPS
        prev_time = now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if init.display.current_w - 30 <= mouse[0] <= init.display.current_w - 10 and 10 <= mouse[1] <= 30:
                    sys.exit()
                else:
                    if mouse[0] < init.display.current_w * 0.8:
                        new_rect = pygame.draw.rect(screen, (0, 0, 0), (predator1.x - position.x, predator1.y - position.y, predator1.IMG.get_width() * init.zoom, init.zoom * predator1.IMG.get_height()), 5, 3)
                        if new_rect.collidepoint(mouse[0], mouse[1]):
                            init.selected = True, predator1
                            prey_selected = True
                        elif not prey_selected:
                            for prey in preys:
                                new_rect = pygame.draw.rect(screen, (0, 0, 0), (prey.x - position.x, prey.y - position.y, prey.IMG.get_width() * init.zoom, init.zoom * prey.IMG.get_height()), 5, 3)
                                if new_rect.collidepoint(mouse[0], mouse[1]):
                                    init.selected = True, prey
                        if not prey_selected :
                            for predator in predators:
                                new_rect = pygame.draw.rect(screen, (0, 0, 0), (predator.x - position.x, predator.y - position.y, predator.IMG.get_width() * init.zoom, init.zoom * predator.IMG.get_height()), 5, 3)
                                if new_rect.collidepoint(mouse[0], mouse[1]):
                                    init.selected = True, predator
                        prey_selected = False
                    else:
                        if init.buttons_position["plus_button"][0] <= mouse[0] <= init.buttons_position["plus_button"][0] + 15 and init.buttons_position["plus_button"][1] <= mouse[1] <= init.buttons_position["plus_button"][1] + 15:
                            zooming_in = True
                        elif init.buttons_position["minus_button"][0] <= mouse[0] <= init.buttons_position["minus_button"][0] + 15 and init.buttons_position["minus_button"][1] <= mouse[1] <= init.buttons_position["minus_button"][1] + 15:
                            zooming_out = True
                        elif init.buttons_position["default_button"][0] <= init.mouse[0] <= init.buttons_position["default_button"][0] + init.font2.size("Default")[0] and init.buttons_position["default_button"][1] <= init.mouse[1] <= init.buttons_position["default_button"][1] + init.font2.size("Default")[1]:
                            zooming_default =True
                        elif init.buttons_position["cancel_selected"][0] <= init.mouse[0] <= init.buttons_position["cancel_selected"][0] + 15 and init.buttons_position["cancel_selected"][1] <= init.mouse[1] <= init.buttons_position["cancel_selected"][1] + 15:
                            init.selected = False, None
                        elif init.buttons_position["show_hide_graph"][0][0] <= init.mouse[0] <= init.buttons_position["show_hide_graph"][0][0] + init.font2.size("show")[0] and init.buttons_position["show_hide_graph"][0][1] <= init.mouse[1] <= init.buttons_position["show_hide_graph"][0][1] + init.font2.size("A")[1]:
                            init.buttons_position["show_hide_graph"] = init.buttons_position["show_hide_graph"][0], not init.buttons_position["show_hide_graph"][1]
                        elif init.buttons_position["show_hide_predators_preys_status"][0][0] <= init.mouse[0] <= init.buttons_position["show_hide_predators_preys_status"][0][0] + init.font2.size("show")[0] and init.buttons_position["show_hide_predators_preys_status"][0][1] <= init.mouse[1] <= init.buttons_position["show_hide_predators_preys_status"][0][1] + init.font2.size("A")[1]:
                            init.buttons_position["show_hide_predators_preys_status"] = init.buttons_position["show_hide_predators_preys_status"][0] ,not init.buttons_position["show_hide_predators_preys_status"][1]
                        elif init.buttons_position["up_prey"][0][0] <= init.mouse[0] <= init.buttons_position["up_prey"][0][0] + 15 and init.buttons_position["up_prey"][0][1] <= init.mouse[1] <= init.buttons_position["up_prey"][0][1] + 15:
                            init.buttons_position["up_prey"] = init.buttons_position["up_prey"][0] ,not init.buttons_position["up_prey"][1]
                            if init.up_down_prey // 2 + 18 < len(preys):
                                init.up_down_prey += 2
                            print(init.up_down_prey)

                        elif init.buttons_position["side_bar_prey"][4]:

                            if init.buttons_position["side_bar_prey"][0][0] <= mouse[0] <= init.buttons_position["side_bar_prey"][3][0] and init.buttons_position["side_bar_prey"][0][1] <= mouse[1] <= init.buttons_position["side_bar_prey"][3][1]:
                                if init.buttons_position["side_bar_prey"][0][0] <= mouse[0] <= init.buttons_position["side_bar_prey"][2][0] and init.buttons_position["side_bar_prey"][0][1] <= mouse[1] <= init.buttons_position["side_bar_prey"][1][1]:
                                    percent = 100 - (100 * (mouse[1] - init.buttons_position["side_bar_prey"][0][1]) / (init.buttons_position["side_bar_prey"][1][1] - init.buttons_position["side_bar_prey"][0][1]))
                                    percent = abs(percent) * 2 / 100
                                    init.up_down_prey = max(init.up_down_prey - 2 * round(5 * percent), 0)
                                elif init.buttons_position["side_bar_prey"][0][0] <= mouse[0] <= init.buttons_position["side_bar_prey"][2][0] and init.buttons_position["side_bar_prey"][2][1] <= mouse[1] <= init.buttons_position["side_bar_prey"][3][1]:
                                    percent = 100 * (mouse[1] - init.buttons_position["side_bar_prey"][2][1]) / (init.buttons_position["side_bar_prey"][3][1] -init.buttons_position["side_bar_prey"][2][1])
                                    percent = abs(percent) * 2 / 100

                                    print(init.up_down_prey, init.up_down_prey + 2 * round(5 * percent))
                                    init.up_down_prey = min(init.up_down_prey + 2 * round(5 * percent), (len(preys) - 18)  *2)
                                    print(init.up_down_prey)
                                    if init.up_down_prey < 0: init.up_down_prey = 0
                                    print(init.up_down_prey)
                                    print("-*-*-*--*-")





            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    init.menu = True

                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_LEFT:
                    camera_rect.left = camera_rect.left - 100
                    position.x = camera_rect.left - camera_borders['left']
                elif event.key == pygame.K_RIGHT:
                    camera_rect.left = camera_rect.left + 100
                    position.x = camera_rect.left - camera_borders['left']
                elif event.key == pygame.K_UP:
                    camera_rect.top = camera_rect.top - 100
                    position.y = camera_rect.top - camera_borders['top']
                elif event.key == pygame.K_DOWN:
                    camera_rect.top = camera_rect.top + 100
                    position.y = camera_rect.top - camera_borders['top']
                elif event.key == pygame.K_SPACE:
                    preys, predators = spawn_more_obj(init, preys, predators)
        if pause: continue
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            predator1.angle += 10
        elif keys[pygame.K_d]:
            predator1.angle -= 10
        elif keys[pygame.K_w]:
            moving = True
            predator1.moveUp()
            preys = predator1.eat(preys, init)
            # predators = predator1.eat(predators, init)
        if not moving:
            predator1.slowObject()

        preys, predators = check_eat(preys, predators, init)

        screen.fill((50, 50, 50))

        if zooming_in:
            init.zoom *= 2
            predator1.scale((2, 2))
            predator1.max_vel *= 2
            predator1.acceleration *= 2
            predator1.x, predator1.y = predator1.x * 2, predator1.y * 2
            background_image = pygame.transform.scale_by(background_image, (2, 2))
        elif zooming_out:
            init.zoom /= 2
            predator1.scale((0.5, 0.5))
            predator1.max_vel /= 2
            predator1.acceleration /= 2
            predator1.x, predator1.y = predator1.x / 2, predator1.y / 2
            background_image = pygame.transform.scale_by(background_image, (0.5, 0.5))
        elif zooming_default:
            predator1.img = init.predator1_original_img
            predator1.max_vel /= init.zoom
            predator1.x, predator1.y = predator1.x / init.zoom, predator1.y / init.zoom
            predator1.rect = pygame.Rect(predator1.x, predator1.y, predator1.img.get_size()[0], predator1.img.get_size()[1])

            background_image = init.background_original_img

        screen.blit(background_image, (0 - position.x, 0 - position.y))

        predator1.draw(screen, position)

        # threads = []
        for prey in preys:
            prey.update()
            if zooming_in:
                prey.scale((2, 2))
                prey.max_vel *= 2
                prey.x, prey.y = prey.x * 2, prey.y * 2
                prey.rect = pygame.Rect(prey.x, prey.y, prey.img.get_size()[0], prey.img.get_size()[1])
            elif zooming_out:
                prey.scale((0.5, 0.5))
                prey.max_vel /= 2
                prey.x, prey.y = prey.x / 2, prey.y / 2
                prey.rect = pygame.Rect(prey.x, prey.y, prey.img.get_size()[0], prey.img.get_size()[1])
            elif zooming_default:
                prey.img = init.prey_original_img
                prey.max_vel /= init.zoom
                prey.x, prey.y = prey.x / init.zoom, prey.y / init.zoom
                prey.rect = pygame.Rect(prey.x, prey.y, prey.img.get_size()[0], prey.img.get_size()[1])

            prey.draw(screen, position)
        for predator in predators:
            predator.update()
            if zooming_in:
                predator.scale((2, 2))
                predator.max_vel *= 2
                predator.x, predator.y = predator.x * 2, predator.y * 2
                predator.rect = pygame.Rect(predator.x, predator.y, predator.img.get_size()[0], predator.img.get_size()[1])
            elif zooming_out:
                predator.scale((0.5, 0.5))
                predator.max_vel /= 2
                predator.x, predator.y = predator.x / 2, predator.y / 2
                predator.rect = pygame.Rect(predator.x, predator.y, predator.img.get_size()[0], predator.img.get_size()[1])

            elif zooming_default:
                predator.img = init.predator_original_img
                predator.max_vel /= init.zoom
                predator.x, predator.y = predator.x / init.zoom, predator.y / init.zoom
                predator.rect = pygame.Rect(predator.x, predator.y, predator.img.get_size()[0], predator.img.get_size()[1])
            predator.draw(screen, position)

        """
        for thread in threads:
            thread.join()
        for prey in preys:
            prey.draw(screen)
        """
        pygame.draw.rect(screen, (255, 255, 255), (0 - position.x, 0 - position.y, init.cage[0], init.cage[1]), 2, 2)

        #  old camera
        # if init.selected[0]:
        #     if selected.x - position.x != background_image.get_width() / (4 * init.zoom):
        #         position.x += selected.x - (position.x + background_image.get_width() / (4 * init.zoom))
        #     if selected.y - position.y != background_image.get_height() / (4 * init.zoom):
        #         position.y += selected.y - (position.y + background_image.get_height() / (4 * init.zoom))
        #     data_panel(screen, selected, init.cage)
        #     pygame.draw.rect(screen, (0, 0, 0), (selected.x - position.x, selected.y - position.y, selected.IMG.get_width() * init.zoom, init.zoom * selected.IMG.get_height()), 2*init.zoom, 3)

        if init.selected[0]:
            if init.selected[1].x < camera_rect.left:
                camera_rect.left = init.selected[1].x
            if init.selected[1].y < camera_rect.top:
                camera_rect.top = init.selected[1].y
            if init.selected[1].x + init.selected[1].img.get_size()[0] > camera_rect.right:
                camera_rect.right = init.selected[1].x + init.selected[1].img.get_size()[0]
            if init.selected[1].y + init.selected[1].img.get_size()[1] > camera_rect.bottom:
                camera_rect.bottom = init.selected[1].y + init.selected[1].img.get_size()[1]
            position.x = camera_rect.left - camera_borders['left']
            position.y = camera_rect.top - camera_borders['top']
            data_panel(screen, init.selected[1], init.cage)
            pygame.draw.rect(screen, (0, 0, 0), (init.selected[1].x - position.x, init.selected[1].y - position.y, init.selected[1].IMG.get_width() * init.zoom, init.zoom * init.selected[1].IMG.get_height()), int (2 * init.zoom), 3)

        map_panel(screen, preys, predators, init.cage, init, position)
        init.clock.tick(500)

        draw(screen, init, preys, predators)
        pygame.display.update()

        if zooming_default:
            init.zoom = 1
            zooming_default = False

        zooming_in = False
        zooming_out = False

if __name__ == '__main__':
    main()
