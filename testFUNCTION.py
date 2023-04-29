import pickle
import random
import sys
import math
import pygame, time
from pygame.locals import Rect


def addBuckt(vecter, init, objInBuckts):
    width = math.ceil(init.cage[0] / init.cel_size)
    cell_position = int(math.floor((vecter[0]) / init.cel_size) + math.floor((vecter[1]) / init.cel_size) * width)
    if cell_position < 0:
        print("celposition : ", cell_position, "vector ", vecter)
    if not cell_position in objInBuckts:
        objInBuckts.append(cell_position)

    return objInBuckts


def addBuckt2(vecter, init, objInBuckts):
    width = math.ceil(init.cage[0] / init.cel_size)

    cell_position = int(math.floor((vecter[0]) / init.cel_size) + math.floor((vecter[1]) / init.cel_size) * width)
    objInBuckts.append(cell_position)

    if not (cell_position + 1) % width == 0 or cell_position == 0:
        objInBuckts.append(cell_position + 1)
        if cell_position + init.cols in init.buckets:
            objInBuckts.append(cell_position + init.cols + 1)
        if cell_position - init.cols in init.buckets:
            objInBuckts.append(cell_position - init.cols + 1)
    if not cell_position % width == 0:
        objInBuckts.append(cell_position - 1)
        if cell_position + init.cols in init.buckets:
            objInBuckts.append(cell_position + init.cols - 1)
        if cell_position - init.cols in init.buckets:
            objInBuckts.append(cell_position - init.cols - 1)

    if cell_position + init.cols in init.buckets:
        objInBuckts.append(cell_position + init.cols)
    if cell_position - init.cols in init.buckets:
        objInBuckts.append(cell_position - init.cols)

    return objInBuckts

def get_id_for_obj(init, obj):
    list = []
    list = addBuckt((obj.rect.left, obj.rect.top), init, list)
    list = addBuckt((obj.rect.right, obj.rect.top), init, list)
    list = addBuckt((obj.rect.left, obj.rect.bottom), init, list)
    list = addBuckt((obj.rect.right, obj.rect.bottom), init, list)
    return list

def register_obj(init, obj):
    obj_cell_ids = get_id_for_obj(init, obj)
    for i in obj_cell_ids:
        if i < 0: continue
        if not i in init.buckets:
            init.selected = True, obj
            # init.pause = True
        else:
            init.buckets[i].append(obj)


def get_near_by_obj(init, obj):
    list = []
    if obj.x < 0:
        obj.x = 10
    if obj.y < 0:
        obj.y = 10
    obj_in_bucket = get_id_for_obj(init, obj)
    for i in obj_in_bucket:
        if i < 0:
            init.selected = True, obj
            continue
        if not i in init.buckets:
            # init.selected = True, obj
            # init.pause = True
            # print(init.cage[0], init.cage[1])
            # print(obj.x, obj.y, i)
            pass
        else:
            list += init.buckets[i]
    while obj in list:
        list.remove(obj)
    if len(list) == 0:
        return []
    else:
        return list


def get_near_by_obj2(init, obj):
    list = []
    l = addBuckt2((obj.rect.left, obj.rect.top), init, [])
    for i in l:
        if not i in init.buckets:
            init.selected = True, obj
            # init.pause = True
            print(init.cage[0], init.cage[1])
            print(obj.x, obj.y, l)
            break
        else:
            list += init.buckets[i]
    while obj in list:
        list.remove(obj)
    if len(list) == 0:
        return []
    else:
        return list


def update_lines(screen, near_by_list, obj, position, init, zoom):
    from Class import Predator

    i = 0
    if type(obj) == Predator:
        lines_angle = 30
        lines_angle_pluse = 6.6
    else:
        lines_angle = 150
        lines_angle_pluse = 33.3

    for j in range(9):
        if j <= 2: power = 5
        elif j <= 5: power = 1
        else: power = 5

        angle = - lines_angle + i
        i += lines_angle_pluse
        radians = math.radians(angle - obj.angle - 90)
        vertical = math.cos(radians) * (150 * zoom)
        horizontal = math.sin(radians) * (150 * zoom)
        new_line = (obj.x + obj.rect.width / 2, obj.y + obj.rect.height / 2), (obj.x + vertical, obj.y + horizontal)
        enemy = False
        closest = 150
        closest_type = None
        closest_coordinates = ((0, 0), (0, 0))
        for k in range(len(near_by_list)):
            coordinates = near_by_list[k].rect.clipline(new_line)
            if coordinates:
                enemy = True
                current = math.sqrt((coordinates[0][0] - new_line[0][0]) ** 2 + (coordinates[0][1] - new_line[0][1]) ** 2)
                if closest > current:
                    # if obj == init.selected[1]:
                    #     print(closest, current)
                    closest = current
                    closest_coordinates = coordinates
                else:
                    continue
                if type(near_by_list[k]) == Predator:
                    closest_type = "Predator"
                    obj.input[j * 2] = closest
                    if type(obj) == Predator:
                        obj.input[j * 2 + 1] = - 1 * power
                    else:
                        obj.input[j * 2 + 1] = -2 * power

                else:
                    closest_type = "Prey"
                    obj.input[j * 2] = closest
                    if type(obj) == Predator:
                        obj.input[j * 2 + 1] = 2 * power
                    else:
                        obj.input[j * 2 + 1] = 1 * power

        if not enemy:
            wall = False
            for p in range(len(init.walls)):
                a = init.walls[p].clipline(new_line)
                if a:

                    wall = True
                    current = math.sqrt((a[0][0] - new_line[0][0]) ** 2 + (a[0][1] - new_line[0][1]) ** 2)
                    obj.input[j * 2] = max(current, 20)
                    obj.input[j * 2 + 1] = 0
                    if obj == init.selected[1]:
                        pygame.draw.line(screen, (255, 255, 0), (new_line[0][0] - position.x, new_line[0][1] - position.y), (a[0][0] - position.x, a[0][1] - position.y), 1)
                    break
            if not wall:
                obj.input[j * 2] = 150
                obj.input[j * 2 + 1] = 0
                if obj == init.selected[1]:
                    pygame.draw.line(screen, (255, 255, 255), (new_line[0][0] - position.x, new_line[0][1] - position.y), (new_line[1][0] - position.x, new_line[1][1] - position.y), 1)

        elif closest < 150:
            if obj == init.selected[1]:
                coordinates = closest_coordinates
                if closest_type == "Predator":
                    pygame.draw.line(screen, (255, 0, 0), (new_line[0][0] - position.x, new_line[0][1] - position.y), (coordinates[0][0] - position.x, coordinates[0][1] - position.y), 1)
                else:
                    pygame.draw.line(screen, (0, 255, 0), (new_line[0][0] - position.x, new_line[0][1] - position.y), (coordinates[0][0] - position.x, coordinates[0][1] - position.y), 1)
        # if obj == init.selected[1]:
        #     print(obj.input)
        #     print(obj.nn.forward_pass(obj.input))


def scale_image(image, factor):
    size = round(image.get_width() * factor), round(image.get_height() * factor)
    return pygame.transform.scale(image, size)


def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)


def draw(screen, init, preys, predators):
    # move this position to Inint class
    right_panel = pygame.Surface((init.display.current_w * 0.2, init.display.current_h * 0.7))
    right_panel.fill((100, 0, 0))
    right_panel.set_alpha(128)
    fps_text = init.font.render(f'FPS : {round(init.clock.get_fps())}', True, (255, 255, 255))
    # screen.blit(init.menu_background, (init.display.current_w * 0.8, 0))
    top_right_panel = pygame.Surface((init.display.current_w * 0.2, init.display.current_h * 0.3))
    top_right_panel.fill((10, 10, 10))
    top_right_panel.set_alpha(128)
    screen.blit(top_right_panel, (init.display.current_w * 0.8, 0))
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, 0), (init.display.current_w * 0.8, init.display.current_h), 2)
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, init.display.current_h * 0.3), (init.display.current_w, init.display.current_h * 0.3), 2)

    if init.buttons_position["show_hide_graph"][1]:
        now = time.time()
        second = now - init.prev_time
        graph_prey = pygame.Surface((right_panel.get_width() * 0.8, right_panel.get_height() * 0.3))
        graph_prey.fill((0, 0, 0))
        prey_text_number = init.font2.render(f"Prey  :  {len(init.preys)}", True, (255, 255, 255))
        graph_prey.blit(prey_text_number, (5, 5))
        pygame.draw.rect(graph_prey, (255, 255, 255), (0, 0, graph_prey.get_width(), graph_prey.get_height()), 2, 2)
        pygame.draw.line(graph_prey, (255, 255, 255), (0, init.font2.size("A")[1] + 7), (graph_prey.get_width(), init.font2.size("A")[1] + 7), 2)

        graph_predator = pygame.Surface((right_panel.get_width() * 0.8, right_panel.get_height() * 0.3))
        graph_predator.fill((0, 8, 0))
        predators_text_number = init.font2.render(f"Predator  :  {len(init.predators)}", True, (255, 255, 255))
        graph_predator.blit(predators_text_number, (5, 5))


        max_changed = False
        max_changed_predator = False
        if second >= 0.5:
            init.half_seceond_passed = not init.half_seceond_passed
            init.prev_time = now

            if init.max_preys < len(init.preys):
                init.m = init.max_preys
                max_changed = True
                init.max_preys = len(init.preys)
            if init.max_predators < len(init.predators):
                init.m_predator = init.max_predators
                max_changed_predator = True
                init.max_predators = len(init.predators)

        if init.half_seceond_passed:
            size_preys = (init.font2.size("A")[1] + 9) + (graph_prey.get_height() * 0.9) - ((len(init.preys) / init.max_preys) * (graph_prey.get_height() * 0.9))
            init.graph_prey_lines.append([(graph_prey.get_width() - 2, graph_prey.get_height() - 2), (graph_prey.get_width() - 2, size_preys - 2), len(init.preys)])
            for element in init.graph_prey_lines:
                if max_changed:
                    size_preys = (init.font2.size("A")[1] + 9) + (graph_prey.get_height() * 0.9) - (
                            (element[2] / init.max_preys) * (graph_prey.get_height() * 0.9)) - 2
                    element[0] = element[0][0] - 2, element[0][1]
                    element[1] = element[1][0] - 2, size_preys
                else:
                    element[0] = element[0][0] - 2, element[0][1]
                    element[1] = element[1][0] - 2, element[1][1]
            if init.graph_prey_lines[0][0][0] == 0:
                init.graph_prey_lines.pop(0)


            size_predators = (init.font2.size("A")[1] + 9) + (graph_predator.get_height() * 0.9) - ((len(init.predators) / init.max_predators) * (graph_predator.get_height() * 0.9))
            init.graph_predator_lines.append([(graph_predator.get_width() - 2, graph_predator.get_height() - 2), (graph_predator.get_width() - 2, size_predators - 2), len(init.predators)])
            for element in init.graph_predator_lines:
                if max_changed_predator:
                    size_predators = (init.font2.size("A")[1] + 9) + (graph_predator.get_height() * 0.9) - (
                            (element[2] / init.max_predators) * (graph_predator.get_height() * 0.9)) - 2
                    element[0] = element[0][0] - 2, element[0][1]
                    element[1] = element[1][0] - 2, size_predators
                else:
                    element[0] = element[0][0] - 2, element[0][1]
                    element[1] = element[1][0] - 2, element[1][1]
            if init.graph_predator_lines[0][0][0] == 0:
                init.graph_predator_lines.pop(0)

            init.half_seceond_passed = False

        if len(init.graph_prey_lines) != 0:
            for element in init.graph_prey_lines:
                pygame.draw.line(graph_prey, (0, 255, 0), element[0], element[1], 2)
        if len(init.graph_predator_lines) != 0:
            for element in init.graph_predator_lines:
                pygame.draw.line(graph_predator, (255, 0, 0), element[0], element[1], 2)
        right_panel.blit(graph_predator, (right_panel.get_width() * 0.1, right_panel.get_height() * 0.1))
        right_panel.blit(graph_prey, (right_panel.get_width() * 0.1, right_panel.get_height() * 0.6))

        pygame.draw.line(right_panel, (255, 255, 255), (0, right_panel.get_height() * 0.5), (right_panel.get_width(), right_panel.get_height() * 0.5), 2)



    screen.blit(init.name_text, (init.display.current_w - (init.name_text.get_width() + 35), 10))
    screen.blit(init.exit_btn, (init.display.current_w - 30, 10))
    # screen.blit(fps_text, (10, 10))

    if init.zoom < 1:
        zoom = - 1 / init.zoom
    else:
        zoom = init.zoom
    zoom_text = init.font2.render(f'Zoom :  {round(zoom)}', True, (255, 255, 255))
    screen.blit(zoom_text, (init.display.current_w * 0.81, init.display.current_h * 0.1))

    plus_button = pygame.image.load("images/plus_btn.png")
    screen.blit(plus_button, (init.display.current_w * 0.82 + init.font2.size(f'Zoom : {round(init.zoom)}')[0], init.display.current_h * 0.1 + 5))
    minus_button = pygame.image.load("images/minus_btn.png")
    screen.blit(minus_button, (init.display.current_w * 0.84 + init.font2.size(f'Zoom : {round(init.zoom)}')[0], init.display.current_h * 0.1 + 5))

    if init.buttons_position["default_button"][0] <= init.mouse[0] <= init.buttons_position["default_button"][0] + init.font2.size("Default")[0] and init.buttons_position["default_button"][1] <= init.mouse[1] <= init.buttons_position["default_button"][1] + init.font2.size("Default")[1]:
        default_text = init.font2.render('Default', True, (255, 0, 0))
    else:
        default_text = init.font2.render('Default', True, (255, 255, 255))
    if init.selected[0]:
        s_text = f'Selected  :  {init.selected[1].name}'
        selected_text = init.font2.render(s_text, True, (255, 255, 255))
        if init.buttons_position["cancel_selected"][0] <= init.mouse[0] <= init.buttons_position["cancel_selected"][0] + 15 and init.buttons_position["cancel_selected"][1] <= init.mouse[1] <= init.buttons_position["cancel_selected"][1] + 15:
            cancel_button = pygame.image.load("images/cancel_button_red.png")
            screen.blit(cancel_button, (init.display.current_w * 0.81 + init.font2.size(s_text)[0] + 10,
                                        init.display.current_h * 0.1 + init.font2.size("A")[1] + 5))

        else:
            cancel_button = pygame.image.load("images/cancel_button.png")
            screen.blit(cancel_button, (init.display.current_w * 0.81 + init.font2.size(s_text)[0] + 10,
                                        init.display.current_h * 0.1 + init.font2.size("A")[1] + 5))
    else:
        s_text = f'Selected  : None'
        selected_text = init.font2.render(s_text, True, (180, 180, 180))
    screen.blit(selected_text, (init.display.current_w * 0.81, init.display.current_h * 0.1 + init.font2.size("A")[1] * 1))
    init.buttons_position["cancel_selected"] = (init.display.current_w * 0.81 + init.font2.size(s_text)[0] + 10, init.display.current_h * 0.1 + init.font2.size("A")[1] + 5)
    graph_text = init.font2.render("graphs : ", True, (255, 255, 255))
    preys_and_predators_text = init.font2.render("Preys and Predators :  ", True, (255, 255, 255))
    if init.buttons_position["show_hide_predators_preys_status"][1]:
        preys_and_predators_status = "hide"
        status_preys_predators = pygame.Surface((right_panel.get_width() * 0.9, right_panel.get_height() * 0.90))
        status_preys_predators.fill((0, 0, 0))
        preys_status_title = init.font2.render(f"Preys  :  {len(init.preys)}", True, (255, 255, 255))
        predators_status_title = init.font2.render(f"Predators  :  {len(init.predators)}", True, (255, 255, 255))
        right_panel.blit(preys_status_title, (right_panel.get_width() * 0.05, right_panel.get_height() * 0.02))
        right_panel.blit(predators_status_title, (right_panel.get_width() * 0.55, right_panel.get_height() * 0.02))
        # pygame.draw.line(status_preys_predators, (255, 255, 255), (status_preys_predators.get_width() * 0.5, 0),(status_preys_predators.get_width() * 0.5, status_preys_predators.get_height()), 2)
        pygame.draw.rect(status_preys_predators, (255, 255, 255), (0, 0, status_preys_predators.get_width(), status_preys_predators.get_height()), 2, 2)
        if init.buttons_position["up_prey"][0][0] <= init.mouse[0] <= init.buttons_position["up_prey"][0][0] + 15 and init.buttons_position["up_prey"][0][1] <= init.mouse[1] <= init.buttons_position["up_prey"][0][1] + 15:
            up_button = pygame.image.load("images/up_red.png")
        else:
            up_button = pygame.image.load("images/up_white.png")
        j = -1

        for i in range(init.up_down_prey, 40 + init.up_down_prey, 2):
            if (i) // 2 < len(preys):
                status_preys_predators.blit(init.font.render(preys[(i) // 2].name + f"   health : {preys[(i) // 2].health}", True, (255, 255, 255)), (status_preys_predators.get_width() * 0.1, 5 + (i - init.up_down_prey - 0.5) * init.font.size("A")[1]))
                pygame.draw.line(status_preys_predators, (255, 255, 255), (init.font.size(preys[(i) // 2].name + f"   health : {preys[(i) // 2].health}")[0] + status_preys_predators.get_width() * 0.15, (i - init.up_down_prey - 0.5) * init.font.size("A")[1] - 20),
                                 (status_preys_predators.get_width(), (i - init.up_down_prey - 0.5) * init.font.size("A")[1] - 20), 2)
                status_preys_predators.blit(init.font.render(f"speed : {round(preys[(i) // 2].vel, 2)} , age : {round(preys[(i) // 2].birthday - time.time())} ", True, (255, 255, 255)), (status_preys_predators.get_width() * 0.1, 5 + ((i - init.up_down_prey - 0.5) + 1) * init.font.size("A")[1]))

        pygame.draw.line(status_preys_predators, (255, 255, 255), (status_preys_predators.get_width() * 0.04, status_preys_predators.get_height() * 0.1), (status_preys_predators.get_width() * 0.04, status_preys_predators.get_height() - status_preys_predators.get_height() * 0.04),
                         round(status_preys_predators.get_width() * 0.04))
        prey_side_bar = status_preys_predators.get_height() - status_preys_predators.get_height() * 0.04 - (status_preys_predators.get_height() * 0.1)
        if len(preys) == 0:
            size = 1
        else:
            size = len(preys)
        prey_side_bar_start = (status_preys_predators.get_height() * 0.1) + (init.up_down_prey * 100 / (size * 2)) * (prey_side_bar / 100)
        prey_side_bar_end = (34 * 100 / (size * 2)) * (prey_side_bar / 100) + prey_side_bar_start
        if len(preys) < 18:
            pygame.draw.line(status_preys_predators, (255, 0, 0), (status_preys_predators.get_width() * 0.04, status_preys_predators.get_height() * 0.1), (status_preys_predators.get_width() * 0.04, status_preys_predators.get_height() - status_preys_predators.get_height() * 0.04),
                             round(status_preys_predators.get_width() * 0.04))
        else:
            pygame.draw.line(status_preys_predators, (255, 0, 0), (status_preys_predators.get_width() * 0.04, prey_side_bar_start), (status_preys_predators.get_width() * 0.04, prey_side_bar_end), round(status_preys_predators.get_width() * 0.04))

        down_button = pygame.transform.rotate(pygame.image.load("images/up_white.png"), 180)

        status_preys_predators.blit(up_button, (status_preys_predators.get_width() * 0.02, status_preys_predators.get_height() * 0.02))
        status_preys_predators.blit(down_button, (status_preys_predators.get_width() * 0.02, status_preys_predators.get_height() * 0.05))
        right_panel.blit(status_preys_predators, (right_panel.get_width() * 0.05, right_panel.get_height() * 0.07))
        init.buttons_position["side_bar_prey"] = [
            (-(round(status_preys_predators.get_width() * 0.04) / 2) + right_panel.get_width() * 0.05 + init.display.current_w * 0.8 + status_preys_predators.get_width() * 0.04, right_panel.get_height() * 0.07 + init.display.current_h * 0.3 + status_preys_predators.get_height() * 0.1),
            (-(round(status_preys_predators.get_width() * 0.04) / 2) + right_panel.get_width() * 0.05 + init.display.current_w * 0.8 + status_preys_predators.get_width() * 0.04, right_panel.get_height() * 0.07 + init.display.current_h * 0.3 + prey_side_bar_start), (
                -(round(status_preys_predators.get_width() * 0.04) / 2) + right_panel.get_width() * 0.05 + init.display.current_w * 0.8 + status_preys_predators.get_width() * 0.04 + round(status_preys_predators.get_width() * 0.04),
                right_panel.get_height() * 0.07 + init.display.current_h * 0.3 + prey_side_bar_end), (
                -(round(status_preys_predators.get_width() * 0.04) / 2) + right_panel.get_width() * 0.05 + init.display.current_w * 0.8 + status_preys_predators.get_width() * 0.04 + round(status_preys_predators.get_width() * 0.04),
                right_panel.get_height() * 0.07 + init.display.current_h * 0.3 + status_preys_predators.get_height() - status_preys_predators.get_height() * 0.04), True]
    else:
        init.buttons_position["side_bar_prey"] = [None, None, None, None, False]
        preys_and_predators_status = "show"
    if init.display.current_w * 0.81 + init.font2.size("Preys and Predators :  ")[0] <= init.mouse[0] <= init.display.current_w * 0.81 + init.font2.size("Preys and Predators :  ")[0] + init.font2.size("hide")[0] and init.display.current_h * 0.1 + init.font2.size("a")[1] * 3 <= init.mouse[
        1] <= init.display.current_h * 0.1 + init.font2.size("A")[1] * 4:
        preys_and_predators_text_status = init.font2.render(preys_and_predators_status, True, (255, 0, 0))
    else:
        preys_and_predators_text_status = init.font2.render(preys_and_predators_status, True, (255, 255, 255))
    screen.blit(preys_and_predators_text_status, (init.display.current_w * 0.81 + init.font2.size("Preys and Predators :  ")[0], init.display.current_h * 0.1 + init.font2.size("a")[1] * 3))
    if init.buttons_position["show_hide_graph"][1]:
        show_graph = "hide"

    else:
        show_graph = "show"
    if init.buttons_position["show_hide_graph"][0][0] <= init.mouse[0] <= init.buttons_position["show_hide_graph"][0][0] + init.font2.size("show")[0] and init.buttons_position["show_hide_graph"][0][1] <= init.mouse[1] <= init.buttons_position["show_hide_graph"][0][1] + init.font2.size("A")[1]:
        graph_text_show_hide = init.font2.render(show_graph, True, (255, 0, 0))
    else:
        graph_text_show_hide = init.font2.render(show_graph, True, (255, 255, 255))
    screen.blit(graph_text, (init.display.current_w * 0.81,
                             init.display.current_h * 0.1 + init.font2.size("A")[1] * 2))
    screen.blit(graph_text_show_hide, (init.display.current_w * 0.81 + init.font2.size("show graph : ")[0] + 5,
                                       init.display.current_h * 0.1 + init.font2.size("A")[1] * 2))
    screen.blit(preys_and_predators_text, (init.display.current_w * 0.81,
                                           init.display.current_h * 0.1 + init.font2.size("A")[1] * 3))
    screen.blit(default_text, (init.buttons_position["minus_button"][0] + 30, init.display.current_h * 0.1))
    screen.blit(right_panel, (init.display.current_w * 0.8, init.display.current_h * 0.3))
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, 0), (init.display.current_w * 0.8, init.display.current_h), 2)
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, init.display.current_h * 0.3), (init.display.current_w, init.display.current_h * 0.3), 2)


def map_panel(screen, preys, predators, cage, init, position):
    map_width = screen.get_width() * 0.2
    map_height = screen.get_height() * 0.2
    panel = pygame.Surface((map_width, map_height))

    panel.set_alpha(128)
    panel.fill((0, 0, 0))
    for prey in preys:
        pygame.draw.line(screen, (0, 255, 0), (((prey.x * 100) / cage[0]) * (screen.get_width() * 0.2) / 100, screen.get_height() - screen.get_height() * 0.2 + (((prey.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100),
                         ((((prey.x * 100) / cage[0]) * (screen.get_width() * 0.2)) / 100, screen.get_height() - screen.get_height() * 0.2 + (((prey.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), 2)
    for predator in predators:
        pygame.draw.line(screen, (255, 0, 0), (((predator.x * 100) / cage[0]) * (screen.get_width() * 0.2) / 100, screen.get_height() - screen.get_height() * 0.2 + (((predator.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100),
                         ((((predator.x * 100) / cage[0]) * (screen.get_width() * 0.2)) / 100, screen.get_height() - screen.get_height() * 0.2 + (((predator.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), 2)
    x_100_percent = position.x / cage[0] / 0.01
    y_100_percent = position.y / cage[1] / 0.01
    width_100_percent = screen.get_width() / cage[0] / 0.01
    height_100_percent = screen.get_height() / cage[1] / 0.01
    x_new = x_100_percent * map_width / 100
    y_new = y_100_percent * map_height / 100
    width_new = width_100_percent * map_width / 100
    height_new = height_100_percent * map_height / 100
    pygame.draw.rect(panel, (255, 0, 0), (x_new, y_new, width_new, height_new), 2, 2)
    screen.blit(panel, (0, screen.get_height() - screen.get_height() * 0.2))


def data_panel(screen, selected, cage):
    from Class import Prey
    panel = pygame.Surface((200, 190))
    panel.set_alpha(128)
    panel.fill((0, 0, 0))
    screen.blit(panel, (screen.get_width() * 0.2 + 5, screen.get_height() - screen.get_height() * 0.2))
    x = (selected.health * 48) / 100
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() * 0.2 + 89, screen.get_height() - screen.get_height() * 0.2 + 19, x + 2, 10), 2, 2)
    x = (selected.health * 48) / 100
    health_bar = pygame.Surface((x, 8))
    health_bar.set_alpha(128)
    health_bar.fill((60, 255, 60))
    screen.blit(health_bar, (screen.get_width() * 0.2 + 90, screen.get_height() - screen.get_height() * 0.2 + 20))
    font = pygame.font.Font('font/cc-ultimatum-bold.otf', 15)
    # status = font.render(f"status : \nvel : {selected.vel}\nAngle : {selected.angle}\nposition : {selected.x}, {selected.y}", True, (255, 255, 255))
    hp = font.render(f"HP : {selected.health}", True, (255, 255, 255))
    screen.blit(hp, (screen.get_width() * 0.2 + 25, screen.get_height() - screen.get_height() * 0.2 + 17))
    # screen.blit(status, (20, screen.get_height() - 170))
    if type(selected) == Prey:
        status = f"status : \nvel : {selected.vel}\nAngle : {round(selected.angle)}\nposition : {round(selected.x)}, {round(selected.y)}, \ndt : {selected.dt}"
    else:
        status = f"status : \nvel : {selected.vel}\nAngle : {round(selected.angle)}\nposition : {round(selected.x)}, {round(selected.y)}, \ndt : {selected.dt}, \nkills : {selected.kills}, \nage : {selected.age}"
    render_multi_line(screen, font, status, screen.get_width() * 0.2 + 25, screen.get_height() - screen.get_height() * 0.2 + 40, 15)


def render_multi_line(screen, font, text, x, y, fsize):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        screen.blit(font.render(l, 0, (255, 255, 255)), (x, y + fsize * i))


def set_preys_predators(init):
    from Class import NN,Prey, Predator
    preys = []
    predators = []
    if init.zoom_type == "IN":
        zoom = init.zoom
    elif init.zoom_type == "OUT":
        zoom = 1 / init.zoom
    else:
        zoom = 1
    for e in range(int(init.data[0])):
        prey = Prey(float(init.data[1]), float(init.data[2]))
        prey.scale((zoom, zoom))
        prey.x = random.randrange(0, init.cage[0] - prey.img.get_size()[0])
        prey.y = random.randrange(0, init.cage[1] - prey.img.get_size()[1])
        prey.angle = random.randrange(0, 360)
        prey.name = "Prey_" + str(e)
        prey.nn = NN()
        preys.append(prey)
    for e in range(int(init.data[3])):
        predator = Predator(float(init.data[4]), float(init.data[5]))
        predator.scale((zoom, zoom))
        predator.x = random.randrange(0, init.cage[0] - predator.img.get_size()[0])
        predator.y = random.randrange(0, init.cage[1] - predator.img.get_size()[1])
        predator.angle = random.randrange(0, 360)
        predator.name = "Predator_" + str(e)
        predator.nn = NN()
        predators.append(predator)
    return preys, predators


def spawn_more_obj(init, preys, predators, nmbr_prey, nmbr_predator):
    from Class import NN,Prey, Predator
    if init.zoom_type == "IN":
        zoom = init.zoom
    elif init.zoom_type == "OUT":
        zoom = 1 / init.zoom
    else:
        zoom = 1
    pickle_in_preys = open("best_data_preys.pickle", "rb")
    preys_best = pickle.load(pickle_in_preys)
    preys_weight = [array[0] for array in preys_best]
    preys_bias = [array[1] for array in preys_best]
    for e in range(nmbr_prey):
        prey = Prey(float(init.data[1]), float(init.data[2]))
        prey.scale((zoom, zoom))
        prey.x = random.randrange(0, init.cage[0] - prey.img.get_size()[0])
        prey.y = random.randrange(0, init.cage[1] - prey.img.get_size()[1])
        prey.name = "Prey_" + str(e + int(init.data[0]))
        prey.nn = NN()
        prey.nn.weight = preys_weight[e % len(preys_weight)]
        prey.nn.bias = preys_bias[e % len(preys_bias)]
        prey.angle = random.randrange(0, 360)

        preys.append(prey)
    if nmbr_prey !=0:
        init.data[0] = str(int(init.data[0]) + e + 1)
    pickle_in_predators = open("best_data_predators.pickle", "rb")
    predators_best = pickle.load(pickle_in_predators)
    predators_weight = [predator[0] for predator in predators_best]
    predators_bias = [predator[1] for predator in predators_best]
    for e in range(nmbr_predator):
        predator = Predator(float(init.data[4]), float(init.data[5]))
        predator.scale((zoom, zoom))
        predator.x = random.randrange(0, init.cage[0] - predator.img.get_size()[0])
        predator.y = random.randrange(0, init.cage[1] - predator.img.get_size()[1])
        predator.name = "Predator_" + str(e + int(init.data[3]))
        predator.nn = NN()
        predator.nn.weight = predators_weight[e % len(predators_weight)]
        predator.nn.bias = predators_bias[e % len(predators_bias)]
        predator.angle = random.randrange(0, 360)

        predators.append(predator)
    if nmbr_predator !=0:
        init.data[3] = str(int(init.data[3]) + e + 1)
    return preys, predators


def menu_panel(screen, init):
    from Class import background_objects_class
    # menu_background = pygame.image.load('images/menu_background.jpg')
    # menu_background = pygame.transform.scale(menu_background, (init.display.current_w, init.display.current_h))
    # init.menu_background = menu_background

    title = init.font3.render("Prey VS Predators", True, (0, 255, 0))
    prey_title = init.font3.render("Prey", True, (255, 255, 255))
    predator_title = init.font3.render("Predator", True, (255, 255, 255))
    moving_speed = init.font2.render("moving speed : ", True, (255, 255, 255))
    rotation_speed = init.font2.render("rotation speed : ", True, (255, 255, 255))
    map_size = init.font2.render("map size : ", True, (255, 255, 255))
    population_number = init.font2.render("population number : ", True, (255, 255, 255))
    writing_in = -1
    writing_this = init.data
    # background_objects_rect = []
    # background_objects = []
    # for i in range(50):
    #     background_objects_rect.append(Rect(random.randint(100, init.display.current_w - 100), random.randint(100, init.display.current_h - 100), random.randint(0, 70), random.randint(0, 70)))
    #     obj = background_objects_class()
    #     background_objects.append(obj)
    prev_time = time.time()
    half_seceond_passed = False
    matrix_time = time.time()
    matrix_time_2 = time.time()
    one_second_passed = False
    font = pygame.font.Font('font/SourceHanSerifSC-Regular.otf', 15)
    font.set_bold(True)
    font_glow = pygame.font.Font('font/SourceHanSerifSC-Regular.otf', 18)
    font_glow.set_bold(True)
    j = 1
    matrix = ["你", "好", "世", "界", "中", "文", "程", "序", "列", "表", "函", "数", "类", "对象", "模", "块", "字", "符", "串"]
    index = random.randrange(0, len(matrix) - 1)
    while True:
        # screen.blit(menu_background, (0, 0))
        screen.fill((0, 0, 0))
        # for i in range(len(background_objects)):
        #     if init.display.current_w - 70 <= background_objects_rect[i].left:
        #         background_objects_rect[i].left = 70
        #     elif 70 >= background_objects_rect[i].right:
        #             background_objects_rect[i].left = init.display.current_w - 70
        #     elif init.display.current_h - 70 <= background_objects_rect[i].top :
        #         background_objects_rect[i].top = 70
        #     elif 70 >= background_objects_rect[i].bottom:
        #         background_objects_rect[i].top = init.display.current_h - 70
        #     if i != len(background_objects):
        #         index = pygame.Rect.collidelist(background_objects_rect[i], background_objects_rect[i+1:])
        #
        #         if index != -1:
        #             background_objects[i].angel = random.uniform(-360, 360)
        #             background_objects[i].direction *= -1
        #
        #
        #     background_objects[i].speed_x = random.uniform(0, 2)
        #     background_objects[i].speed_y = random.uniform(0, 2)
        #     if background_objects[i].speed_x == 0 and background_objects[i].speed_y == 0:
        #         background_objects[i].speed_x = random.uniform(1, 2)
        #         background_objects[i].speed_y = random.uniform(1, 2)
        #     radians = math.radians(background_objects[i].angel)
        #     vertical = math.cos(radians) * background_objects[i].speed_x
        #     horizontal = math.sin(radians) * background_objects[i].speed_y
        #     background_objects_rect[i].left -= vertical * background_objects[i].direction
        #     background_objects_rect[i].top -= horizontal * background_objects[i].direction
        #     pygame.draw.rect(screen, (255, 255, 255), background_objects_rect[i], 2)

        now = time.time()
        second = now - prev_time
        if second >= 0.3:
            half_seceond_passed = not half_seceond_passed
            prev_time = now
        if time.time() - matrix_time >= 0.05:
            matrix_time = time.time()
            j += 1
        if time.time() - matrix_time_2 >= 0.7:
            matrix_time_2 = time.time()
            index = random.randrange(0, len(matrix) - 1)

            one_second_passed = True

        for k in range(0, init.display.current_w, 10):

            for i in range(0, 10):



                if i == 9:
                    glow = pygame.Surface((18, 18))
                    glow.fill((0, 0, 0))
                    glow.set_alpha(200)

                    glow.blit(font_glow.render(matrix[index * i % len(matrix)], True, (0, 255, 0)), (0, 0))
                    screen.blit(glow, (10 + (k * 10), (15 * (i + 1) + j * 10 + k * 5) % init.display.current_h))
                screen.blit(font.render(matrix[index * i % len(matrix)], True, (0 , 100 + (i * 15), 0)), (10 + (k * 5), (15 * (i + 1) + j * 10 + k * 10) % init.display.current_h))
            for i in range(0, 10):

                if i == 9:
                    glow = pygame.Surface((18, 18))
                    glow.fill((0, 0, 0))
                    glow.set_alpha(200)

                    glow.blit(font_glow.render(matrix[index * i % len(matrix)], True, (0, 255, 0)), (0, 0))
                    screen.blit(glow, (10 + (k * 10), (15 * (i + 1) + j * 10 + k * 2) % init.display.current_h))
                screen.blit(font.render(matrix[index * i % len(matrix)], True, (0, 100 + (i * 10), 0)), (10 + (k * 2), (15 * (i + 1) + j * 20 + (k // 2) * 50) % init.display.current_h))

            # pygame.draw.rect(screen, (0, 20 + (i * 20), 0), (10, (10 * (i + 1) + j * 10) % init.display.current_h, 10, 10))
        population_number_text_prey = init.font2.render(writing_this[0], True, (255, 255, 255))
        moving_speed_text_prey = init.font2.render(writing_this[1], True, (255, 255, 255))
        rotation_speed_text_prey = init.font2.render(writing_this[2], True, (255, 255, 255))
        population_number_text_predator = init.font2.render(writing_this[3], True, (255, 255, 255))
        moving_speed_text_predator = init.font2.render(writing_this[4], True, (255, 255, 255))
        rotation_speed_text_predator = init.font2.render(writing_this[5], True, (255, 255, 255))
        map_size_text = init.font2.render(writing_this[6], True, (255, 255, 255))

        mouse = pygame.mouse.get_pos()

        menu_panel = pygame.Surface((init.display.current_w * 0.8, init.display.current_h * 0.8))
        menu_panel.set_alpha(150)

        screen.blit(menu_panel, (init.display.current_w * 0.1, init.display.current_h * 0.1))
        screen.blit(title, ((init.display.current_w * 0.1) + (menu_panel.get_width() / 2) - init.font3.size("prey VS predators")[0] / 2, (init.display.current_h * 0.1) + 20))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.1, init.display.current_h * 0.1, init.display.current_w * 0.8, init.display.current_h * 0.8), 2, 2)

        screen.blit(prey_title, (init.display.current_w * 0.15, init.display.current_h * 0.32))
        screen.blit(population_number, (init.display.current_w * 0.15, init.display.current_h * 0.4))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
        screen.blit(population_number_text_prey, (init.display.current_w * 0.3 + 5, init.display.current_h * 0.4))
        screen.blit(moving_speed, (init.display.current_w * 0.15, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
        screen.blit(moving_speed_text_prey, (init.display.current_w * 0.3 + 5, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2))
        screen.blit(rotation_speed, (init.display.current_w * 0.15, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
        screen.blit(rotation_speed_text_prey, (init.display.current_w * 0.3 + 5, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4))

        pygame.draw.line(screen, (255, 255, 255), (init.display.current_w / 2, init.display.current_h * 0.2), (init.display.current_w / 2, init.display.current_h * 0.8), 2)

        screen.blit(predator_title, (init.display.current_w * 0.55, init.display.current_h * 0.32))
        screen.blit(population_number, (init.display.current_w * 0.55, init.display.current_h * 0.4))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.70, init.display.current_h * 0.4, 100, init.font2.size("a")[1]), 2, 2)
        screen.blit(population_number_text_predator, (init.display.current_w * 0.70 + 5, init.display.current_h * 0.4))
        screen.blit(moving_speed, (init.display.current_w * 0.55, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2, 100, init.font2.size("a")[1]), 2, 2)
        screen.blit(moving_speed_text_predator, (init.display.current_w * 0.70 + 5, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2))
        screen.blit(rotation_speed, (init.display.current_w * 0.55, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4, 100, init.font2.size("a")[1]), 2, 2)
        screen.blit(rotation_speed_text_predator, (init.display.current_w * 0.70 + 5, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4))

        screen.blit(map_size, (init.display.current_w * 0.15, init.display.current_h * 0.82))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.23 - 2, init.display.current_h * 0.82, 100, init.font2.size("a")[1] + 3), 2, 2)
        screen.blit(map_size_text, (init.display.current_w * 0.23 + 5, init.display.current_h * 0.82 + 1))

        if init.display.current_w * 0.82 - 5 <= mouse[0] <= init.display.current_w * 0.82 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:
            start_text = init.font2.render("Start", True, (255, 255, 255))
            start_button = pygame.Surface((init.font2.size("Start")[0] + 17, init.font2.size("Start")[1] + 7))
            start_button.fill((0, 0, 0))
        else:
            start_text = init.font2.render("Start", True, (0, 0, 0))
            start_button = pygame.Surface((init.font2.size("Start")[0] + 17, init.font2.size("Start")[1] + 7))
            start_button.fill((255, 255, 255))
        screen.blit(start_button, (init.display.current_w * 0.82 - 3, init.display.current_h * 0.82 + 2))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.82 - 5, init.display.current_h * 0.82, init.font2.size("Start")[0] + 20, init.font2.size("Start")[1] + 10), 2, 4)
        screen.blit(start_text, (init.display.current_w * 0.82 + 4, init.display.current_h * 0.82 + 4))

        if init.display.current_w * 0.75 - 5 <= mouse[0] <= init.display.current_w * 0.75 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:
            exit_text = init.font2.render("Exit", True, (255, 255, 255))
            exit_button = pygame.Surface((init.font2.size("Start")[0] + 17, init.font2.size("Start")[1] + 7))
            exit_button.fill((255, 0, 0))
        else:
            exit_text = init.font2.render("Exit", True, (0, 0, 0))
            exit_button = pygame.Surface((init.font2.size("Start")[0] + 17, init.font2.size("Start")[1] + 7))
            exit_button.fill((255, 255, 255))
        screen.blit(exit_button, (init.display.current_w * 0.75 - 3, init.display.current_h * 0.82 + 2))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.75 - 5, init.display.current_h * 0.82, init.font2.size("Start")[0] + 20, init.font2.size("Start")[1] + 10), 2, 4)
        screen.blit(exit_text, (init.display.current_w * 0.75 - 3 + (init.font2.size("Start")[0] + 17) / 2 - (init.font2.size("Exit")[0]) / 2, init.display.current_h * 0.82 + 4))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if init.display.current_w * 0.3 <= mouse[0] <= init.display.current_w * 0.3 + 100 and init.display.current_h * 0.4 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1]:
                    writing_in = 0
                elif init.display.current_w * 0.3 <= mouse[0] <= init.display.current_w * 0.3 + 100 and init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 + init.font2.size("a")[1]:
                    writing_in = 1
                elif init.display.current_w * 0.3 <= mouse[0] <= init.display.current_w * 0.3 + 100 and init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 + init.font2.size("a")[1]:
                    writing_in = 2
                elif init.display.current_w * 0.70 <= mouse[0] <= init.display.current_w * 0.70 + 100 and init.display.current_h * 0.4 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1]:
                    writing_in = 3
                elif init.display.current_w * 0.70 <= mouse[0] <= init.display.current_w * 0.70 + 100 and init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 + init.font2.size("a")[1]:
                    writing_in = 4
                elif init.display.current_w * 0.70 <= mouse[0] <= init.display.current_w * 0.70 + 100 and init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 <= mouse[1] <= init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 + init.font2.size("a")[1]:
                    writing_in = 5
                elif init.display.current_w * 0.23 - 2 <= mouse[0] <= init.display.current_w * 0.23 + 100 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("a")[1] + 3:
                    writing_in = 6
                elif init.display.current_w * 0.82 - 5 <= mouse[0] <= init.display.current_w * 0.82 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:
                    init.menu = False
                    init.data = writing_this
                    init.max_preys = int(writing_this[0])
                    init.m = init.max_preys
                    return True
                elif init.display.current_w * 0.75 - 5 <= mouse[0] <= init.display.current_w * 0.75 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:
                    sys.exit()
                else:
                    writing_in = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and writing_in != -1:
                    writing_in = -1
                if event.key == pygame.K_ESCAPE:
                    init.menu = False
                    if init.cage[0] == 0:
                        sys.exit()
                    else:
                        return False
                elif event.key == pygame.K_BACKSPACE and writing_in != -1:
                    writing_this[writing_in] = writing_this[writing_in][:-1]
                elif writing_in != -1 and len(writing_this[writing_in]) < 7:
                    writing_this[writing_in] += event.unicode
        if writing_in != -1:
            if writing_in == 0:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 + 5 + init.font2.size(writing_this[0])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 1:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 + 5 + init.font2.size(writing_this[1])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] * 3 - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 2:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 + 5 + init.font2.size(writing_this[2])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] * 5 - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 3:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4, 100, init.font2.size("a")[1]), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70 + 5 + init.font2.size(writing_this[3])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 4:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2, 100, init.font2.size("a")[1]), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70 + 5 + init.font2.size(writing_this[4])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] * 3 - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 5:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4, 100, init.font2.size("a")[1]), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.7 + 5 + init.font2.size(writing_this[5])[0], init.display.current_h * 0.4 + init.font2.size("a")[1] * 5 - 4, init.font2.size("a")[0], 2), 2)
            elif writing_in == 6:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.23 - 2, init.display.current_h * 0.82, 100, init.font2.size("a")[1] + 3), 2, 2)
                if half_seceond_passed: pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.23 + 5 + init.font2.size(writing_this[6])[0], init.display.current_h * 0.82 + init.font2.size("a")[1] - 4, init.font2.size("a")[0], 2), 2)

        pygame.display.update()
        init.clock.tick(500)


def get_list_rect(list):
    l = []
    for element in list:
        l.append(element.rect)
    return l


def check_eat_collide(init):
    from Class import Predator, Prey
    one_secend_passed = False
    if time.time() - init.time >= 1:
        init.time = time.time()
        one_secend_passed = True
    size = len(init.predators)
    i = 0
    while i < size:
        predator = init.predators[i]
        if one_secend_passed:
            # predator.age += 1
            predator.health -= 4
            if predator.health <= 0:
                if predator == init.selected[1]:
                    init.selected = False, None
                save = [
                    predator.nn.weight,
                    predator.nn.bias,
                    predator.kills,
                    predator.age
                ]
                init.saved_predators.append(save)
                init.predators.pop(i)
                size -= 1

                continue
        list = get_near_by_obj(init, predator)
        while predator in list:
            list.remove(predator)
        list_rect = get_list_rect(list)
        index = pygame.Rect.collidelistall(predator.rect, list_rect)
        # if init.selected[1] == predator:
        #     for l in range(len(list_rect)):
        #         pygame.draw.rect(init.screen, (255, 255, 255), (list_rect[l].left - init.position[0], list_rect[l].top - init.position[1], predator.img.get_size()[0], predator.img.get_size()[1]), 2)
        if index is not None:
            for element in index:
                obj = list[element]
                if type(obj) == Prey:
                    prey = obj
                    prey.health -= 50
                    predator.angle += 180
                    predator.vel = 1
                    predator.move()
                    predator.vel = 0
                    predator.angle -= 180
                    if prey.health == 0:
                        if prey == init.selected[1]:
                            init.selected = False, None
                        if prey in init.preys:
                            save = [
                                prey.nn.weight,
                                prey.nn.bias,
                                prey.age
                            ]
                            init.saved_preys.append(save)
                            init.preys.remove(prey)
                        if init.up_down_prey - 2 >= 0: init.up_down_prey -= 2
                        predator.kills += 1
                        if predator.health + 30 > 200:
                            predator.health = 200
                        else:
                            predator.health += 20
                elif type(obj) == Predator:
                    predator.angle += 180
                    predator.vel *= 2
                    predator.move()
                    predator.vel = 0
                    predator.angle -= 180
        i += 1
    for i in range(len(init.preys)):
        prey = init.preys[i]
        # if one_secend_passed: prey.age += 1
        list = get_near_by_obj(init, prey)
        while prey in list:
            list.remove(prey)
        list_rect = get_list_rect(list)
        index = pygame.Rect.collidelistall(prey.rect, list_rect)
        if index != None:
            for element in index:
                obj = list[element]
                if type(obj) == Predator:
                    prey.angle += 180
                    prey.vel = 2
                    prey.move()
                    prey.vel = 0
                    prey.angle -= 180
                    predator = obj
                    predator.health -= 5
                    if predator.health <= 0:
                        if predator == init.selected[1]:
                            init.selected = False, None
                        if predator in init.predators:
                            save = [
                                predator.nn.weight,
                                predator.nn.bias,
                                predator.kills,
                                predator.age
                            ]
                            init.saved_predators.append(save)
                            init.predators.remove(predator)
                elif type(obj) == Prey:

                    prey.angle += 180
                    prey.vel *= 4
                    prey.move()
                    prey.vel = 0
                    prey.angle -= 180

