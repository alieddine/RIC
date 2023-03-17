import pygame
import random
import math


def is_inside_view_cone(starting_point, cone_min_vec, cone_max_vec, point_to_test):
    vector_to_point = [point_to_test[0] - starting_point[0], point_to_test[1] - starting_point[1]]

    cross_1 = cone_min_vec[0] * vector_to_point[1] - cone_min_vec[1] * vector_to_point[0]
    cross_2 = cone_max_vec[0] * vector_to_point[1] - cone_max_vec[1] * vector_to_point[0]

    dot_1 = cone_min_vec[0] * vector_to_point[0] + cone_min_vec[1] * vector_to_point[1]

    if cross_1 < 0 < cross_2 or cross_1 > 0 > cross_2 and dot_1 > 0:
        return True
    else:
        return False


class Point:
    def __init__(self, x, y):
        self.point = [x, y]


pygame.init()
screen = pygame.display.set_mode((800,600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color("#000000"))

running = True
start_point = (400, 300)
view_cone_max_end_point = [-900.0, -400.0]
view_cone_min_end_point = [-500.0, -900.0]

view_cone_max = [view_cone_max_end_point[0] - start_point[0],
                 view_cone_max_end_point[1] - start_point[1]]

view_cone_min = [view_cone_min_end_point[0] - start_point[0],
                 view_cone_min_end_point[1] - start_point[1]]

test_points = []
for _ in range(0, 100):
    test_points.append(Point(random.randint(10, 790), random.randint(10, 590)))

clock = pygame.time.Clock()
point = [200, 300]
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                vec_to_mouse = [mouse_pos[0] - start_point[0], mouse_pos[1] - start_point[1]]
                length = math.sqrt(vec_to_mouse[0]**2 + vec_to_mouse[1]**2)
                vec_to_mouse_norm = [vec_to_mouse[0]/length, vec_to_mouse[1]/length]

                min_cone_norm = [vec_to_mouse_norm[0] * math.cos(math.pi/6) - vec_to_mouse_norm[1] * math.sin(math.pi/6),
                                 vec_to_mouse_norm[0] * math.sin(math.pi/6) + vec_to_mouse_norm[1] * math.cos(math.pi/6)]

                max_cone_norm = [
                    vec_to_mouse_norm[0] * math.cos(-math.pi / 6) - vec_to_mouse_norm[1] * math.sin(-math.pi / 6),
                    vec_to_mouse_norm[0] * math.sin(-math.pi / 6) + vec_to_mouse_norm[1] * math.cos(-math.pi / 6)]

                view_cone_min = [min_cone_norm[0]*1000, min_cone_norm[1]*1000]
                view_cone_max = [max_cone_norm[0]*1000, max_cone_norm[1]*1000]

                view_cone_max_end_point = [start_point[0] + view_cone_max[0], start_point[1] + view_cone_max[1]]
                view_cone_min_end_point = [start_point[0] + view_cone_min[0], start_point[1] + view_cone_min[1]]
            if event.button == 3:
                start_point = pygame.mouse.get_pos()
                view_cone_max_end_point = [start_point[0] + view_cone_max[0], start_point[1] + view_cone_max[1]]
                view_cone_min_end_point = [start_point[0] + view_cone_min[0], start_point[1] + view_cone_min[1]]

    screen.blit(background, (0, 0))
    pygame.draw.line(screen, pygame.Color("#FFFFFF"), start_point, view_cone_max_end_point)
    pygame.draw.line(screen, pygame.Color("#FFFFFF"), start_point, view_cone_min_end_point)

    for point in test_points:
        test_point = point.point
        if is_inside_view_cone(start_point, view_cone_min, view_cone_max, test_point):
            pygame.draw.line(screen, pygame.Color("#0000FF"), test_point, [test_point[0] + 1, test_point[1] + 1], 2)
        else:
            pygame.draw.line(screen, pygame.Color("#FF0000"), test_point, [test_point[0] + 1, test_point[1] + 1], 2)

    pygame.display.flip()

pygame.quit()