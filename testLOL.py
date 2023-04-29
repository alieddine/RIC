import math
import random
import threading, queue


from testFUNCTION import *
import pygame, time
import sys
import numpy as np
from Class import *
import pickle
from genitic import genitic_fun


def main():
    pygame.init()
    init = Init()

    screen = pygame.display.set_mode((init.display.current_w, init.display.current_h), pygame.FULLSCREEN)
    init.screen = screen
    prev_time = time.time()
    dt = 0
    TARGET_FPS = 60
    background_image = pygame.image.load('images/background.png').convert()
    # background_image = pygame.transform.scale(background_image, (init.display.current_w * 0.8, init.display.current_h))
    background_image = pygame.transform.scale_by(background_image, 3).convert()


    pause = False
    img = scale_image(pygame.image.load("images/test_object.png"), 0.2)

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
    gen = 0
    size = 0
    init.buttons_position["show_hide_graph"] = init.buttons_position["show_hide_graph"][0], True
    start_genetic = True
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
                # init.preys, init.predators = set_preys_predators(init)
                pickle_in_preys = open("best_data_preys.pickle", "rb")
                preys = pickle.load(pickle_in_preys)
                preys_weight = [array[0] for array in preys]
                preys_bias = [array[1] for array in preys]

                pickle_in_predators = open("best_data_predators.pickle", "rb")
                predators = pickle.load(pickle_in_predators)
                predators_weight = [predator[0] for predator in predators]
                predators_bias = [predator[1] for predator in predators]
                init.preys = []
                for i in range(50):
                    prey = Prey(float(init.data[1]), float(init.data[2]))
                    prey.x = random.randrange(100, init.cage[0] - prey.img.get_size()[0]-100)
                    prey.y = random.randrange(100, init.cage[1] - prey.img.get_size()[1]-100)
                    prey.angle = random.randrange(0, 360)
                    prey.name = "Prey_" + str(i)
                    prey.nn = NN()
                    # prey.nn.weight = random.choice(preys_weight)
                    # prey.nn.bias = random.choice(preys_bias)
                    prey.nn.weight = preys_weight[i % len(preys_weight)]
                    prey.nn.bias = preys_bias[i % len(preys_bias)]
                    init.preys.append(prey)
                init.predators = []
                for i in range(20):
                    predator = Predator(float(init.data[1]), float(init.data[2]))
                    predator.x = random.randrange(100, init.cage[0] - predator.img.get_size()[0]-100)
                    predator.y = random.randrange(100, init.cage[1] - predator.img.get_size()[1]-100)
                    predator.angle = random.randrange(0, 360)
                    predator.name = "Predator_" + str(i)
                    predator.nn = NN()
                    # predator.nn.weight = random.choice(predators_weight)
                    # predator.nn.bias = random.choice(predators_bias)
                    predator.nn.weight = predators_weight[i % len(predators_weight)]
                    predator.nn.bias = predators_bias[i % len(predators_bias)]
                    init.predators.append(predator)
            start_time = time.time()
            last_prey = init.preys[-1]
            last_predator = init.predators[-1]
            size = len(init.predators)
            init.prev_time = time.time()
            init.half_seceond_passed = False


        mouse = pygame.mouse.get_pos()
        init.mouse = mouse
        now = time.time()
        Animal.dt = (now - prev_time) * TARGET_FPS
        prev_time = now


        #bucket init
        init.width = init.cage[0]
        init.height = init.cage[1]
        init.cols = math.ceil(init.width / init.cel_size)
        init.rows = math.ceil(init.height / init.cel_size)

        for i in range(init.cols * init.rows):
            init.buckets[i] = []
        for prey in init.preys:
            register_obj(init, prey)
        for predator in init.predators:
            register_obj(init, predator)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if init.display.current_w - 30 <= mouse[0] <= init.display.current_w - 10 and 10 <= mouse[1] <= 30:
                    # if last_prey in init.preys:
                    #     index = init.preys.index(last_prey)
                    # else: index = -1
                    # for i in range(index + 1, len(init.preys)):
                    #     save = [
                    #         init.preys[i].nn.weight,
                    #         init.preys[i].nn.bias,
                    #         init.preys[i].kills,
                    #         init.preys[i].age
                    #     ]
                    #     init.saved_preys.append(save)
                    # if last_predator in init.predators:
                    #     index = init.preys.index(last_predator)
                    # else: index = -1
                    # for i in range(index + 1, len(init.predators)):
                    #     save = [
                    #         init.predators[i].nn.weight,
                    #         init.predators[i].nn.bias,
                    #         init.predators[i].kills,
                    #         init.predators[i].age
                    #     ]
                    #     init.saved_predators.append(save)
                    # print("size ",size, len(init.saved_predators))
                    # pickle_out = open("data_preys.pickle", "wb")
                    # pickle.dump(init.saved_preys, pickle_out)
                    # pickle_out.close()
                    # pickle_out_2 = open("data_predators.pickle", "wb")
                    # pickle.dump(init.saved_predators, pickle_out_2)
                    # pickle_out_2.close()
                    sys.exit()

                else:
                    if mouse[0] < init.display.current_w * 0.8:

                        for prey in init.preys:
                            new_rect = pygame.draw.rect(screen, (0, 0, 0), (prey.x - position.x, prey.y - position.y, prey.IMG.get_width() * init.zoom, init.zoom * prey.IMG.get_height()), 5, 3)
                            if new_rect.collidepoint(mouse[0], mouse[1]):
                                init.selected = True, prey
                                # init.preys.remove(prey)
                                break

                        for predator in init.predators:
                            new_rect = pygame.draw.rect(screen, (0, 0, 0), (predator.x - position.x, predator.y - position.y, predator.IMG.get_width() * init.zoom, init.zoom * predator.IMG.get_height()), 5, 3)
                            if new_rect.collidepoint(mouse[0], mouse[1]):
                                init.selected = True, predator
                                # init.predators.remove(predator)

                                break

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
                            if init.up_down_prey // 2 + 18 < len(init.preys):
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
                                    init.up_down_prey = min(init.up_down_prey + 2 * round(5 * percent), (len(init.preys) - 18)  *2)
                                    print(init.up_down_prey)
                                    if init.up_down_prey < 0: init.up_down_prey = 0
                                    print(init.up_down_prey)
                                    print("-*-*-*--*-")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    init.menu = True

                if event.key == pygame.K_p:
                    init.pause = not init.pause
                if event.key == pygame.K_LEFT:
                    camera_rect.left = camera_rect.left - init.cel_size
                    position.x = camera_rect.left - camera_borders['left']
                elif event.key == pygame.K_RIGHT:
                    camera_rect.left = camera_rect.left + init.cel_size
                    position.x = camera_rect.left - camera_borders['left']
                elif event.key == pygame.K_UP:
                    camera_rect.top = camera_rect.top - init.cel_size
                    position.y = camera_rect.top - camera_borders['top']
                elif event.key == pygame.K_DOWN:
                    camera_rect.top = camera_rect.top + init.cel_size
                    position.y = camera_rect.top - camera_borders['top']
                elif event.key == pygame.K_F1:
                    init.preys, init.predators = spawn_more_obj(init, init.preys, init.predators, 0, 50)
                elif event.key == pygame.K_F2:
                    init.preys, init.predators = spawn_more_obj(init, init.preys, init.predators, 50, 0)
                # elif event.key == pygame.K_RETURN:
                #     start_genetic = True
        if init.pause: continue

        screen.fill((50, 50, 50))
        if zooming_in and (init.zoom_type is None or init.zoom_type == "IN"):
            init.zoom_type = "IN"
            init.zoom *= 2
            init.cel_size *= 2

            background_image = pygame.transform.scale_by(background_image, (2, 2))
            Init.cage = background_image.get_size()

            width = init.cage[0] / init.cel_size
            print(width, init.cage[0], init.cel_size)
        elif zooming_out and (init.zoom_type == None or init.zoom_type == "OUT"):
            init.zoom_type = "OUT"
            init.zoom *= 2
            init.cel_size /= 2
            background_image = pygame.transform.scale_by(background_image, (0.5, 0.5))
            Init.cage = background_image.get_size()
            width = init.cage[0] / init.cel_size
            print(width, init.cage[0], init.cel_size)
        elif zooming_default:
            init.cel_size = 150
            background_image = init.background_original_img
            Init.cage = background_image.get_size()
            width = init.cage[0] / init.cel_size
            print(width, init.cage[0], init.cel_size)
        if init.zoom_type == "IN":
            zoom = init.zoom
        elif init.zoom_type == "OUT":
            zoom = 1 / init.zoom
        else:
            zoom = 1
        screen.blit(background_image, (0 - position.x, 0 - position.y))

        for prey in init.preys:

            if zooming_in and (init.zoom_type is None or init.zoom_type == "IN"):
                init.zoom_type = "IN"
                prey.scale((2, 2))
                prey.max_vel *= 2
                prey.x, prey.y = prey.x * 2, prey.y * 2

            elif zooming_out and (init.zoom_type is None or init.zoom_type == "OUT"):
                init.zoom_type = "OUT"
                prey.scale((0.5, 0.5))
                prey.max_vel //= 2
                prey.x, prey.y = prey.x // 2, prey.y // 2

            elif zooming_default:
                if init.zoom_type == "IN":
                    prey.img = init.prey_original_img
                    prey.max_vel /= init.zoom
                    prey.x, prey.y = prey.x / init.zoom, prey.y / init.zoom
                elif init.zoom_type == "OUT":
                    prey.img = init.prey_original_img
                    prey.max_vel *= init.zoom
                    prey.x, prey.y = prey.x * init.zoom, prey.y * init.zoom

            prey.rect = pygame.Rect(prey.x, prey.y, prey.img.get_size()[0], prey.img.get_size()[1])
            prey.update(zoom)
            prey.draw(screen, position)
        for predator in init.predators:

            if zooming_in and (init.zoom_type is None or init.zoom_type == "IN"):
                predator.scale((2, 2))
                predator.max_vel *= 2
                predator.x, predator.y = predator.x * 2, predator.y * 2
            elif zooming_out and (init.zoom_type is None or init.zoom_type == "OUT"):
                predator.scale((0.5, 0.5))
                predator.max_vel /= 2
                predator.x, predator.y = predator.x / 2, predator.y / 2

            elif zooming_default:
                if init.zoom_type == "IN":
                    predator.img = init.predator_original_img
                    predator.max_vel /= init.zoom
                    predator.x, predator.y = predator.x / init.zoom, predator.y / init.zoom
                elif init.zoom_type == "OUT":
                    predator.img = init.predator_original_img
                    predator.max_vel *= init.zoom
                    predator.x, predator.y = predator.x * init.zoom, predator.y * init.zoom

            predator.rect = pygame.Rect(predator.x, predator.y, predator.img.get_size()[0], predator.img.get_size()[1])
            predator.update(zoom)

            predator.draw(screen, position)

        pygame.draw.rect(screen, (255, 255, 255), (0 - position.x, 0 - position.y, init.cage[0], init.cage[1]), 2, 2)

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
            # pygame.draw.rect(screen, (0, 0, 0), (init.selected[1].x - position.x, init.selected[1].y - position.y, init.selected[1].img.get_width(), init.selected[1].img.get_height()), int(2 * zoom), 3)

        map_panel(screen, init.preys, init.predators, init.cage, init, position)
        init.clock.tick(500)

        draw(screen, init, init.preys, init.predators)
        init.walls = [
            pygame.Rect(0, 0, init.cage[0], 2),
            pygame.Rect(0, 0, 2, init.cage[1]),
            pygame.Rect(init.cage[0], 0, 2, init.cage[1]),
            pygame.Rect(0, init.cage[1], init.cage[0], 2),
        ]

        for prey in init.preys:
            near_by_list = get_near_by_obj2(init, prey)
            update_lines(screen, near_by_list, prey, position, init, zoom)

        for predator in init.predators:
            near_by_list = get_near_by_obj2(init, predator)
            update_lines(screen, near_by_list, predator, position, init, zoom)

        # for i in range(init.cols):
        #     pygame.draw.line(screen, (255, 0, 0), (i * init.cel_size - position.x,  0 - position.y), (i * init.cel_size - position.x, init.cage[1]- position.y), 1)
        # for i in range(init.rows):
        #     pygame.draw.line(screen, (255, 0, 0), (0 - position.x, i * init.cel_size- position.y), (init.cage[0]- position.x, i * init.cel_size- position.y), 1)

        check_eat_collide(init)
        for predator in init.predators:

            if round(predator.age) % 7 == 0:

                wheel = random.randrange(0, 100)
                if len(init.predators) < 20:
                    wheel = random.randrange(0, 49)

                    l = 3
                else: l = 1
                if wheel < 0:
                    save = [
                        predator.nn.weight,
                        predator.nn.bias,
                        predator.kills,
                        predator.age
                    ]
                    init.saved_predators.append(save)
                    init.predators.remove(predator)
                    continue
                if len(init.predators) < 400 and predator.kills != 0 and wheel < 0:
                    for _ in range(l):
                        predator_son = Predator(float(init.data[4]), float(init.data[5]))
                        predator_son.scale((zoom, zoom))
                        if predator.y + predator.img.get_size()[1] + 2 < init.cage[1] - predator.img.get_size()[0]:
                            predator_son.x = predator.x
                            predator_son.y = predator.y + predator.img.get_size()[1] + 2
                        else:
                            predator_son.x = predator.x
                            predator_son.y = predator.y - predator.img.get_size()[1] - 2

                        predator_son.nn = NN()
                        predator_son.nn.weight = random.choice(predators_weight)
                        predator_son.nn.bias = random.choice(predators_bias)
                        predator_son.angle = random.randrange(0, 360)
                        predator.name = "Predator_" + str(init.data[3])
                        init.data[3] = str(int(init.data[3]) + 1)
                        init.predators.append(predator_son)
                        size += 1
        if len(init.predators) == -1:

            for _ in range(10):
                predator_son = Predator(float(init.data[4]), float(init.data[5]))
                predator_son.scale((zoom, zoom))

                predator_son.x = random.randrange(0, init.cage[0] - predator_son.img.get_size()[0])
                predator_son.y = random.randrange(0, init.cage[1] - predator_son.img.get_size()[1])


                predator_son.nn = NN()
                predator_son.nn.weight = random.choice(predators_weight)
                predator_son.nn.bias = random.choice(predators_bias)
                predator_son.angle = random.randrange(0, 360)
                predator.name = "Predator_" + str(init.data[3])
                init.data[3] = str(int(init.data[3]) + 1)
                init.predators.append(predator_son)
        for prey in init.preys:
            if round(prey.age) % 13 == 0:

                wheel = random.randrange(0, 100)

                if len(init.preys) < 5: wheel = 1
                if wheel < 0:
                    save = [
                        prey.nn.weight,
                        prey.nn.bias,
                        prey.age
                    ]
                    init.saved_preys.append(save)
                    init.preys.remove(prey)
                    continue
                if wheel < 0 and len(init.preys) <= 400:
                    prey_son = Prey(float(init.data[1]), float(init.data[2]))
                    prey_son.scale((zoom, zoom))
                    if prey.y + prey.img.get_size()[1] + 2 < init.cage[1] - prey.img.get_size()[0]:
                        prey_son.x = prey.x
                        prey_son.y = prey.y + prey.img.get_size()[1] + 2
                    else:
                        prey_son.x = prey.x
                        prey_son.y = prey.y - prey.img.get_size()[1] - 2

                    prey_son.nn = NN()

                    prey_son.nn.weight = random.choice(preys_weight)
                    prey_son.nn.bias = random.choice(preys_bias)
                    prey_son.angle = random.randrange(0, 360)
                    prey.name = "Prey_" + str(init.data[0])
                    init.data[0] = str(int(init.data[0]) + 1)
                    init.preys.append(prey_son)
        if len(init.preys) == -1:

            for _ in range(10):
                prey_son = Prey(float(init.data[1]), float(init.data[2]))
                prey_son.scale((zoom, zoom))

                prey_son.x = random.randrange(0, init.cage[0] - prey_son.img.get_size()[0])
                prey_son.y = random.randrange(0, init.cage[1] - prey_son.img.get_size()[1])

                prey_son.nn = NN()
                prey_son.nn.weight = random.choice(preys_weight)
                prey_son.nn.bias = random.choice(preys_bias)
                prey_son.angle = random.randrange(0, 360)
                Prey.name = "Preys_" + str(init.data[0])
                init.data[0] = str(int(init.data[0]) + 1)
                init.preys.append(prey_son)
        if len(init.predators) != 0:
            max_kill = max(element.kills for element in init.predators)
        else:
            max_kill = 0
        #     init.selected = False, None

        # for element in init.predators:
        #     if element.kills == max_kill:
        #         init.selected = True, element
        #         break
        fps_text = init.font.render(f'FPS : {round(Animal.dt * init.clock.get_fps())}, gen : {gen}, max kill : {max_kill}', True, (255, 255, 255))

        # screen.blit(fps_text, (10, 10))

        pygame.display.update()

        if zooming_default:
            init.zoom = 1
            zooming_default = False
            init.zoom_type = None

        zooming_in = False
        zooming_out = False
        init.position = position.x, position.y

        if time.time() - start_time >= 50000:
        # if start_genetic:
        #     start_genetic = False
            start_time = time.time()
            if last_prey in init.preys:
                index = init.preys.index(last_prey)
            else: index = -1
            for i in range(len(init.preys)):
                save = [
                    init.preys[i].nn.weight,
                    init.preys[i].nn.bias,
                    init.preys[i].age
                ]
                init.saved_preys.append(save)
            if last_predator in init.predators:
                index = init.predators.index(last_predator)
            else: index = -1
            for i in range(len(init.predators)):
                save = [
                    init.predators[i].nn.weight,
                    init.predators[i].nn.bias,
                    init.predators[i].kills,
                    init.predators[i].age
                ]
                init.saved_predators.append(save)
            print(len(init.saved_predators))
            pickle_out = open("data_preys.pickle", "wb")
            pickle.dump(init.saved_preys, pickle_out)
            pickle_out.close()
            # pickle_out_2 = open("data_predators.pickle", "wb")
            # pickle.dump(init.saved_predators, pickle_out_2)
            # pickle_out_2.close()
            # genitic_fun()
            print(f"gen : {gen}")
            init.saved_predators = []
            init.saved_preys = []
            gen += 1
            pickle_in_preys = open("genitic_data_preys.pickle", "rb")
            preys = pickle.load(pickle_in_preys)
            preys_weight = [array[0] for array in preys]
            preys_bias = [array[1] for array in preys]

            # pickle_in_predators = open("genitic_data_predators.pickle", "rb")
            # predators = pickle.load(pickle_in_predators)
            # predators_weight = [predator[0] for predator in predators]
            # predators_bias = [predator[1] for predator in predators]


            init.preys = []
            for i in range(50):
                prey = Prey(float(init.data[1]), float(init.data[2]))
                prey.scale((zoom, zoom))
                prey.x = random.randrange(100, init.cage[0] - prey.img.get_size()[0]-100)
                prey.y = random.randrange(100, init.cage[1] - prey.img.get_size()[1]-100)
                prey.angle = random.randrange(0, 360)
                prey.name = "Prey_" + str(i)
                prey.nn = NN()
                # prey.nn.weight = random.choice(preys_weight)
                # prey.nn.bias = random.choice(preys_bias)
                prey.nn.weight = preys_weight[i % len(preys_weight)]
                prey.nn.bias = preys_bias[i % len(preys_bias)]
                init.preys.append(prey)
            init.predators = []
            for i in range(20):
                predator = Predator(float(init.data[1]), float(init.data[2]))
                predator.scale((zoom, zoom))
                predator.x = random.randrange(100, init.cage[0] - predator.img.get_size()[0]-100)
                predator.y = random.randrange(100, init.cage[1] - predator.img.get_size()[1]-100)
                predator.angle = random.randrange(0, 360)
                predator.name = "Predator_" + str(i)
                predator.nn = NN()
                # predator.nn.weight = random.choice(predators_weight)
                # predator.nn.bias = random.choice(predators_bias)
                predator.nn.weight = predators_weight[i % len(predators_weight)]
                predator.nn.bias = predators_bias[i % len(predators_bias)]
                init.predators.append(predator)


if __name__ == '__main__':

    main()
    # import cProfile
    # cProfile.run('main()', "output.dat")
    #
    # import pstats
    # from pstats import SortKey
    #
    # with open("output_time.text", "w") as f:
    #     p = pstats.Stats("output.dat", stream=f)
    #     p.sort_stats("time").print_stats()
    #
    # with open("output_calls.text", "w") as f:
    #     p = pstats.Stats("output.dat", stream=f)
    #     p.sort_stats("calls").print_stats()