import math

import pygame
import sys


def main():
    pygame.init()
    # screen = pygame.display.set_mode((1300, 700))
    screen = pygame.display.Info()

    screen = pygame.display.set_mode((screen.current_w, screen.current_h), pygame.FULLSCREEN)
    background_image = pygame.image.load('images/background.png')
    background_image = pygame.transform.scale(background_image, (1300, 700))
    predator = pygame.image.load('images/red_object.png')
    predator = pygame.transform.scale(predator, (25, 25))
    prey = pygame.image.load('images/green_object.png')
    prey = pygame.transform.scale(prey, (30, 25))
    prey = pygame.transform.rotate(prey, 90)
    prey_copy = prey
    clock = pygame.time.Clock()
    i = 0
    j = 0
    x = 70
    y = 350
    pause = False
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_LEFT:
                    j += 20
                    prey_copy = pygame.transform.rotate(prey, j)
                    screen.blit(prey_copy, (70 - int(prey_copy.get_width() / 2), 350 - int(prey_copy.get_height() / 2)))
                    print(j)
                    print("X: ", x, "Y: ", y)

                elif event.key == pygame.K_RIGHT:
                    j -= 20
                    prey_copy = pygame.transform.rotate(prey, j)
                    screen.blit(prey_copy, (70 - int(prey_copy.get_width() / 2), 350 - int(prey_copy.get_height() / 2)))
                    print(j)
                    print("X: ", x, "Y: ", y)
        if pause:
            continue
        x += math.cos(j)
        y += math.sin(j)

        screen.fill((120, 120, 120))

        screen.blit(background_image, (0, 0))
        screen.blit(prey_copy, (x - int(prey_copy.get_width() / 2), y - int(prey_copy.get_height() / 2)))
        screen.blit(predator, (i, 350))
        # i = i + 1
        clock.tick(30)
        pygame.display.update()


if __name__ == '__main__':
    main()
