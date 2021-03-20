import pygame
import random
from Game import Game
from HUD import HUD
pygame.init()

# Fenêtre de base

pygame.display.set_caption("Save the count")  # TODO A changer
screen = pygame.display.set_mode((1024, 576))

running = True  # Jeu en cours

background = pygame.image.load('asset/background.png')

# Création des personnages
game = Game()

hud = HUD(screen)

# toutes les 1 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 1000)

while running:

    # Background
    screen.blit(background, (0, 0))

    # Jack
    screen.blit(game.player.image, game.player.rect)

    # HUD
    hud.refresh()

    # Mouvements de Jack
    if game.pressed.get(pygame.K_RIGHT):
        game.player.right()
    if game.pressed.get(pygame.K_LEFT):
        game.player.left()

    pygame.display.flip()

    for event in pygame.event.get():  # event est une liste

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN : #On appuie sur une touche
            game.pressed[event.key] = True #On reste appuyé sur une touche
        elif event.type == pygame.KEYUP :
            game.pressed[event.key] = False #On lache la touche

        elif event.type == randomVotebarIncrease: # on augmente la barre aléatoirement
            rand = random.random() # nombre entre 0 et 1
            if(rand<0.5): # 50% d'augmenter les bleus
                hud.votebar.blueInc()
            elif(rand<0.7): # 20% d'augmenter les rouges
                hud.votebar.redInc()
