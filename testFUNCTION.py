import random
import sys

import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def draw(screen, init):

    fps_text = init.font.render(f'FPS : {round(init.clock.get_fps())}', True, (255, 255, 255))
    # screen.blit(init.menu_background, (init.display.current_w * 0.8, 0))
    right_panel = pygame.Surface((init.display.current_w * 0.2, init.display.current_h * 0.3))
    right_panel.fill((10, 10, 10))
    right_panel.set_alpha(128)
    screen.blit(right_panel, (init.display.current_w * 0.8, 0))
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, 0), (init.display.current_w * 0.8, init.display.current_h), 2)
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, init.display.current_h * 0.3), (init.display.current_w, init.display.current_h * 0.3), 2)
    if init.right_panel_state:
        right_panel = pygame.Surface((init.display.current_w * 0.2, init.display.current_h * 0.7))
        right_panel.fill((100, 0, 0))
        right_panel.set_alpha(128)
        screen.blit(right_panel, (init.display.current_w * 0.8, init.display.current_h * 0.3))
    screen.blit(init.name_text, (init.display.current_w - (init.name_text.get_width() + 35), 10))
    screen.blit(init.exit_btn, (init.display.current_w - 30, 10))
    screen.blit(fps_text, (10, 10))
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, 0),
                     (init.display.current_w * 0.8, init.display.current_h), 2)
    pygame.draw.line(screen, (255, 255, 255), (init.display.current_w * 0.8, init.display.current_h * 0.3),
                     (init.display.current_w, init.display.current_h * 0.3), 2)
    if init.zoom < 1: zoom = - 1 / init.zoom
    else: zoom = init.zoom
    zoom_text = init.font2.render(f'Zoom :  {round(zoom)}', True, (255, 255, 255))
    screen.blit(zoom_text, (init.display.current_w * 0.81, init.display.current_h * 0.1))

    plus_button = pygame.image.load("images/plus_btn.png")
    screen.blit(plus_button, (init.display.current_w * 0.82 + init.font2.size(f'Zoom : {round(init.zoom)}')[0] , init.display.current_h * 0.1 + 5))
    minus_button = pygame.image.load("images/minus_btn.png")
    screen.blit(minus_button, (init.display.current_w * 0.84 + init.font2.size(f'Zoom : {round(init.zoom)}')[0] , init.display.current_h * 0.1 + 5))
    init.buttons_position["plus_button"] = (init.display.current_w * 0.82 + init.font2.size(f'Zoom : {round(init.zoom)}')[0] , init.display.current_h * 0.1 + 5)
    init.buttons_position["minus_button"] = (init.display.current_w * 0.84 + init.font2.size(f'Zoom : {round(init.zoom)}')[0] , init.display.current_h * 0.1 + 5)
    init.buttons_position["default_button"] = (init.buttons_position["minus_button"][0] + 30, init.display.current_h * 0.1)
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
                                        init.display.current_h * 0.1 + init.font2.size("A")[1] + 15))

        else:
            cancel_button = pygame.image.load("images/cancel_button.png")
            screen.blit(cancel_button, (init.display.current_w * 0.81 + init.font2.size(s_text)[0] + 10,
                                        init.display.current_h * 0.1 + init.font2.size("A")[1] + 15))


    else:
        s_text = f'Selected  : None'
        selected_text = init.font2.render(s_text, True, (180, 180, 180))
    screen.blit(selected_text, (init.display.current_w * 0.81, init.display.current_h * 0.1 + init.font2.size("A")[1] + 10))
    init.buttons_position["cancel_selected"] = (init.display.current_w * 0.81 + init.font2.size(s_text)[0] + 10, init.display.current_h * 0.1 + init.font2.size("A")[1] + 15)




    screen.blit(default_text, (init.buttons_position["minus_button"][0] + 30, init.display.current_h * 0.1))
    init.buttons_position["default_button"] = (init.buttons_position["minus_button"][0] + 30, init.display.current_h * 0.1)


def map_panel(screen , preys, predators, cage):
    panel = pygame.Surface((screen.get_width() * 0.2, screen.get_height() * 0.2))
    panel.set_alpha(128)
    panel.fill((0, 0, 0))
    screen.blit(panel, (0, screen.get_height() - screen.get_height() * 0.2))
    for prey in preys:
        pygame.draw.line(screen, (0, 255, 0), (((prey.x * 100) / cage[0]) * (screen.get_width() * 0.2) / 100, screen.get_height() - screen.get_height() * 0.2 + (((prey.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), ((((prey.x * 100) / cage[0]) * (screen.get_width() * 0.2)) / 100, screen.get_height() - screen.get_height() * 0.2 + (((prey.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), 2)
    for predator in predators:
        pygame.draw.line(screen, (255, 0, 0), (((predator.x * 100) / cage[0]) * (screen.get_width() * 0.2) / 100, screen.get_height() - screen.get_height() * 0.2 + (((predator.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), ((((predator.x * 100) / cage[0]) * (screen.get_width() * 0.2)) / 100, screen.get_height() - screen.get_height() * 0.2 + (((predator.y * 100) / cage[1]) * (screen.get_height() * 0.2)) / 100), 2)


def data_panel(screen, selected, cage):
    panel = pygame.Surface((200, 190))
    panel.set_alpha(128)
    panel.fill((0, 0, 0))
    screen.blit(panel, (screen.get_width() * 0.2 + 5, screen.get_height() - screen.get_height() * 0.2))
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() * 0.2 + 89, screen.get_height() - screen.get_height() * 0.2 + 19, 50, 10), 2, 2)
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
    status = f"status : \nvel : {selected.vel}\nAngle : {round(selected.angle)}\nposition : {round(selected.x)}, {round(selected.y)}, \ndt : {selected.dt}"
    render_multi_line(screen, font, status, screen.get_width() * 0.2 + 25, screen.get_height() - screen.get_height() * 0.2 + 40, 15)


def render_multi_line(screen, font, text, x, y, fsize):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        screen.blit(font.render(l, 0, (255, 255, 255)), (x, y + fsize * i))


def set_preys_predators(init):
    import Class
    preys = []
    predators = []
    for e in range(int(init.data[0])):
        prey = Class.Prey(float(init.data[1]), int(init.data[2]))
        prey.x = random.randrange(Class.Animal.cage[0])
        prey.y = random.randrange(Class.Animal.cage[1])
        prey.name = "Prey_" + str(e)
        preys.append(prey)
    for e in range(int(init.data[3])):
        predator = Class.Predator(int(init.data[4]), int(init.data[5]))
        predator.x = random.randrange(Class.Animal.cage[0])
        predator.y = random.randrange(Class.Animal.cage[1])
        predator.name = "Predator_" + str(e)
        predators.append(predator)
    return preys, predators


def menu_panel(screen, init):
    menu_background = pygame.image.load('images/menu_background.jpg')
    menu_background = pygame.transform.scale(menu_background, (init.display.current_w, init.display.current_h))
    init.menu_background = menu_background

    title = init.font3.render("Prey VS Predators", True, (255, 255, 255))
    prey_title = init.font3.render("Prey", True, (255, 255, 255))
    predator_title = init.font3.render("Predator", True, (255, 255, 255))
    moving_speed = init.font2.render("moving speed : ", True, (255, 255, 255))
    rotation_speed = init.font2.render("rotation speed : ", True, (255, 255, 255))
    population_number = init.font2.render("population number : ", True, (255, 255, 255))
    writing_in = -1
    writing_this = ["50", "0.5", "15", "50", "1", "15"]

    while True:
        population_number_text_prey = init.font2.render(writing_this[0], True, (255, 255, 255))
        moving_speed_text_prey = init.font2.render(writing_this[1], True, (255, 255, 255))
        rotation_speed_text_prey = init.font2.render(writing_this[2], True, (255, 255, 255))
        population_number_text_predator = init.font2.render(writing_this[3], True, (255, 255, 255))
        moving_speed_text_predator = init.font2.render(writing_this[4], True, (255, 255, 255))
        rotation_speed_text_predator = init.font2.render(writing_this[5], True, (255, 255, 255))

        mouse = pygame.mouse.get_pos()
        screen.blit(menu_background, (0, 0))
        screen.fill((40, 40, 40))
        menu_panel = pygame.Surface((init.display.current_w * 0.8, init.display.current_h * 0.8))
        menu_panel.set_alpha(150)

        screen.blit(menu_panel, (init.display.current_w * 0.1, init.display.current_h * 0.1))
        screen.blit(title, ((init.display.current_w * 0.1) + (menu_panel.get_width() / 2) - init.font3.size("prey VS predators")[0] / 2 , (init.display.current_h * 0.1) + 20))
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

        pygame.draw.line(screen, (255, 255, 255), (init.display.current_w / 2, init.display.current_h * 0.2), (init.display.current_w / 2 ,init.display.current_h*0.8), 2)

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
        screen.blit(exit_button, (init.display.current_w * 0.75 - 3, init.display.current_h * 0.82 +2))
        pygame.draw.rect(screen, (255, 255, 255), (init.display.current_w * 0.75 - 5, init.display.current_h * 0.82, init.font2.size("Start")[0] + 20, init.font2.size("Start")[1] + 10), 2, 4)
        screen.blit(exit_text, (init.display.current_w * 0.75 - 3 + (init.font2.size("Start")[0] + 17) / 2 - (init.font2.size("Exit")[0]) / 2 , init.display.current_h * 0.82 + 4))


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
                elif init.display.current_w * 0.82 - 5 <= mouse[0] <= init.display.current_w * 0.82 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:
                    init.menu = False
                    init.data = writing_this
                    return
                elif init.display.current_w * 0.75 - 5 <= mouse[0] <= init.display.current_w * 0.75 - 5 + init.font2.size("Start")[0] + 20 and init.display.current_h * 0.82 <= mouse[1] <= init.display.current_h * 0.82 + init.font2.size("Start")[1] + 10:

                    sys.exit()
                else:
                    writing_in = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and writing_in != -1:
                    writing_in = -1
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE and writing_in != -1:
                    writing_this[writing_in] = writing_this[writing_in][:-1]
                elif writing_in != -1 and len(writing_this[writing_in]) < 8:
                    writing_this[writing_in] += event.unicode
        if writing_in != -1:
            if writing_in == 0:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
            elif writing_in == 1:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
            elif writing_in == 2:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.3 - 2, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4 - 2, 100, init.font2.size("a")[1] + 3), 2, 2)
            elif writing_in == 3:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4, 100, init.font2.size("a")[1]), 2, 2)
            elif writing_in == 4:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 2, 100, init.font2.size("a")[1]), 2, 2)
            elif writing_in == 5:
                pygame.draw.rect(screen, (255, 0, 0), (init.display.current_w * 0.70, init.display.current_h * 0.4 + init.font2.size("a")[1] * 4, 100, init.font2.size("a")[1]), 2, 2)
        screen.blit(init.predator_original_img, (500, 500))
        pygame.display.update()
        init.clock.tick(500)


def check_eat(preys, predators, init):
    init.preys_rect = []
    init.predators_rect = []
    for prey in preys:
        init.preys_rect.append(prey.rect)
    for predator in predators:
        init.predators_rect.append(predator.rect)

    for predator in predators:
        preys = predator.eat(preys, init)
    for prey in preys:
        predators = prey.eat(predators, init)
    return preys, predators