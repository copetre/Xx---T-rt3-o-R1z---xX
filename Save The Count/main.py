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

background = pygame.image.load('asset/hall.jpg')

arrow = pygame.transform.scale(pygame.image.load('asset/arrow.png'),(200,100))

hud = HUD()

# Création des personnages
game = Game(hud)

# toutes les 1 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 1000)

# Sound Bank

channelFond = pygame.mixer.Channel(1)

# Sound at first
channelFond.play(pygame.mixer.Sound('SoundMusic/NiveauBureauVotes2.mp3.ogg'), -1)

while running:
    clock.tick(60)

    # On regarde dans quel niveau on se situe

    screen.blit(background, (0, 0))

    if game.level[0]:

        background = pygame.transform.scale(pygame.image.load('asset/hall.jpg'), (1024, 576))

        if game.player.rect.x > 900 and game.count_policiers == 0 :
            game.level[0] = False
            game.level[1] = True
            game.player.rect.x = 0
            game.spawn_policier()
            game.count_policiers = 1
            game.spawn_senator_red()
            game.count_senator_red = 1


    elif game.level[1]:

        game.player.velocity = 8
        if game.player.rect.x > 900:
            game.level[1] = False
            game.level[2] = True
            game.player.rect.x = 20
            game.spawn_policier()
            game.spawn_matraque()
            game.count_policiers = 2
    elif game.level[2]:
        background = pygame.transform.scale(pygame.image.load('asset/hall.jpg'), (1024, 576))
        if game.player.rect.x > 900:
            game.level[2] = False
            game.level[3] = True
            game.player.rect.x = 20

    elif game.level[3]:
        background = pygame.image.load('asset/hall.jpg')
        if game.player.rect.x > 900:
            game.level[3] = False
            game.level[4] = True
            game.player.rect.x = 0

    elif game.level[4]:
        background = pygame.image.load('asset/exterior.png')
        game.player.rect.x = 0
        
    if game.count_policiers == 0:
        screen.blit(arrow, (800, 200))
    
    # HUD
    hud.refresh(screen)

    # Policiers pan pan
    for police in game.all_policiers:
        # draw policier
        police.refresh(screen)
        police.all_bullets.draw(screen)
        # do actions
        if not(police.dead):
            police.move()
            police.randomFire()
        for bullet in police.all_bullets :
            bullet.move(game.player)

    # Policiers bim bam boum
    for police in game.all_matraque:
        police.refresh(screen)
        # do actions
        if not(police.dead):
            police.move()
            police.randomAttack()

    # Senators
    for senablue in game.all_senblue:
        senablue.refresh(screen)
        if not(senablue.dead):
            senablue.move()

    for senared in game.all_senred:
        senared.refresh(screen)
        if not(senared.dead):
            senared.move()

    # Jack
    game.player.refresh(screen)

    # Mouvements de Jack
    if not(game.player.dead):
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
        # ATTACK
        if game.pressed.get(pygame.K_SPACE):
            game.player.launchAttack()

    pygame.display.flip()

    for event in pygame.event.get():  # event est une liste
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN : #On appuie sur une touche
            game.pressed[event.key] = True #On reste appuyé sur une touche
        elif event.type == pygame.KEYUP :
            game.pressed[event.key] = False #On lache la touche

        elif not(game.player.dead) and event.type == randomVotebarIncrease: # on augmente la barre aléatoirement
            rand = random.random() # nombre entre 0 et 1
            if(rand<0.5): # 50% d'augmenter les bleus
                hud.votebar.blueInc()
            elif (rand < 0.7):  # 20% d'augmenter les rouges
                hud.votebar.redInc()
