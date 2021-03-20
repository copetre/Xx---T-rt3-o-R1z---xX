import pygame
import

pygame.init()

# Fenêtre de base

pygame.display.set_caption("Save the count")  # TODO A changer
screen = pygame.display.set_mode((1024, 576))

running = True  # Jeu en cours

background = pygame.image.load('asset/background.png')

while running:

    screen.blit(background, (0, 0))
    pygame.display.flip()

    for event in pygame.event.get():  # event est une liste

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
