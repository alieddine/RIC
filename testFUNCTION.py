import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def data_panel(screen, selected, cage):
    panel = pygame.Surface((200, 190))
    panel.set_alpha(128)
    panel.fill((0, 0, 0))
    screen.blit(panel, (10, screen.get_height() - 200))
    pygame.draw.rect(screen, (255, 255, 255), (20, screen.get_height() - 190, 50, 10), 2, 2)
    x = (selected.health * 48) / 100
    health_bar = pygame.Surface((x, 8))
    health_bar.set_alpha(128)
    health_bar.fill((60, 255, 60))
    screen.blit(health_bar, (21, screen.get_height() - 189))
    font = pygame.font.Font('font/cc-ultimatum-bold.otf', 15)
    hp = font.render(f"HP : {selected.health}", True, (255, 255, 255))
    screen.blit(hp, (80, screen.get_height() - 190))

