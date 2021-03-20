import pygame
import random
from Game import Game
from HUD import HUD
from Jack import Player
pygame.init()

# Fenêtre de base

pygame.display.set_caption("Save the count")  # TODO A changer
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

running = True  # Jeu en cours

background = pygame.image.load('asset/background.png')

# Création des personnages
game = Game(screen)

hud = HUD(screen)

# toutes les 1 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 1000)

while running:
    clock.tick(60)

    # Background
    screen.blit(background, (0, 0))

    # Jack
    game.player.refresh()

    # HUD
    hud.refresh()

    # Policiers
    game.all_policiers.draw(screen)
    for police in game.all_policiers :
        police.move()

    # Mouvements de Jack

    if game.pressed.get(pygame.K_UP):
        game.player.has_jumped = True

    if game.pressed.get(pygame.K_RIGHT):
        game.player.right()

    else:
        game.player.walkAnimationRight = False

    if game.pressed.get(pygame.K_LEFT):
        game.player.left()
    else:
        game.player.walkAnimationLeft = False

    game.player.jumping()
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
