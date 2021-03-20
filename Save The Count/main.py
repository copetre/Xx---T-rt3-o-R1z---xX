import pygame
import random
from Game import Game
from HUD import HUD
from Jack import Player

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
# Fenêtre de base

pygame.display.set_caption("Save the count")  # TODO A changer
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

running = True  # Jeu en cours

background = pygame.image.load('asset/background.png')

hud = HUD()

# Création des personnages
game = Game(hud)

# toutes les 1 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 1000)

# Sound Bank

channelMove = pygame.mixer.Channel(0)
channelFond = pygame.mixer.Channel(1)
channelPolAtck = pygame.mixer.Channel(2)

# Sound at first
channelFond.play(pygame.mixer.Sound('SoundMusic/NiveauBureauVotes2.mp3.ogg'), -1)

while running:
    clock.tick(60)

    # On regarde dans quel niveau on se situe

    screen.blit(background, (0, 0))

    if game.level[0]:

        background = pygame.transform.scale(pygame.image.load('asset/background.png'), (1024, 576))

        if game.player.rect.x > 900:
            game.level[0] = False
            game.level[1] = True
            game.player.rect.x = 0
            for police in game.all_policiers:
                police.delete_policier()
    elif game.level[1]:
        background = pygame.transform.scale(pygame.image.load('asset/exterior.png'), (1024, 576))

        if game.player.rect.x > 900:
            game.level[1] = False
            game.level[2] = True
            game.player.rect.x = 20
            for police in game.all_policiers:
                police.delete_policier()
    elif game.level[2]:
        background = pygame.transform.scale(pygame.image.load('asset/hall.png'), (1024, 576))
        if game.player.rect.x > 900:
            game.level[2] = False
            game.level[3] = True
            game.player.rect.x = 20
            for police in game.all_policiers:
                police.delete_policier()
    elif game.level[3]:
        background = pygame.transform.scale(pygame.image.load('asset/chamber.png'), (1024, 576))

    # Jack
    game.player.refresh(screen)

    # HUD
    hud.refresh(screen)

    # Policiers
    for police in game.all_policiers:
        police.refresh(screen)
        police.move()
        police.all_bullets.draw(screen)
        police.randomFire()
        channelPolAtck.play(pygame.mixer.Sound('SoundMusic/AttaquePoliciers.ogg'),1)
        for bullet in police.all_bullets :
            bullet.move(game.player)

    # Mouvements de Jack
    if not (game.player.death):
        # JUMP
        if game.pressed.get(pygame.K_UP):
            game.player.jump()
        game.player.gravity()
        # RIGHT
        if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x < 970 :
            game.player.right()
        else:
            game.player.walkAnimationRight = False
        # LEFT
        if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > -10:
            game.player.left()
        else:
            game.player.walkAnimationLeft = False

    pygame.display.flip()

    for event in pygame.event.get():  # event est une liste
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:  # On appuie sur une touche
            game.pressed[event.key] = True  # On reste appuyé sur une touche
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False  # On lache la touche

        elif not (game.player.death) and event.type == randomVotebarIncrease:  # on augmente la barre aléatoirement
            rand = random.random()  # nombre entre 0 et 1
            if (rand < 0.5):  # 50% d'augmenter les bleus
                hud.votebar.blueInc()
            elif (rand < 0.7):  # 20% d'augmenter les rouges
                hud.votebar.redInc()
