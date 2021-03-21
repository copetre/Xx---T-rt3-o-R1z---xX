import pygame
import random
import time
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

background = pygame.image.load('asset/FIRST_SCREEN_1.png')
firstsreen = [pygame.image.load('asset/FIRST_SCREEN_1.png'), pygame.image.load('asset/FIRST_SCREEN_2.png'),pygame.image.load('asset/FIRST_SCREEN_3.png'),pygame.image.load('asset/FIRST_SCREEN_2.png'),]
frame = 0

hud = HUD()

# Création des personnages
game = Game(hud)
arrow = pygame.transform.scale(pygame.image.load('asset/arrow.png'), (200, 100))
# toutes les 1 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 1000)

# Sound Bank

channelFond = pygame.mixer.Channel(1)
channelDoor = pygame.mixer.Channel(7)

# Sound at first
channelFond.play(pygame.mixer.Sound('SoundMusic/NiveauBureauVotes2.mp3.ogg'), -1)

surface = pygame.Surface((800, 90))
surface.fill((128, 128, 128))
rectangle = surface.get_rect(left=100, top=420)  # alternative = (center = (608, 32))
frame = 0

while running:
    clock.tick(60)

    screen.blit(background, (0, 0))

    # Regarde si vivant
    if game.playing and game.player.health == 0 :
        game.playing = False
        hud = HUD()
        game = Game(hud)
    # On regarde dans quel niveau on se situe



    if not game.playing:
        frame = (frame + 1) % 24  # %12 because we have 2 frames * 6 ticks each
        background = firstsreen[frame // 6]
    else:
        if game.level[0] and game.player.rect.x > 900 and game.count_policiers == 0:
            game.level[0] = False
            game.level[1] = True
            for i in game.all_senblue:
                game.delete_senator_blue(i)
            for j in game.all_senred:
                game.delete_senator_red(j)
            channelDoor.play(pygame.mixer.Sound("SoundMusic/Porte.ogg"),0)

            game.player.rect.x = 0

            game.spawn_senator_red(1)
            game.spawn_senator_blue(2)
            game.spawn_policier(1)
            game.spawn_matraque(2)

            background = pygame.transform.scale(pygame.image.load('asset/exterior.jpg'), (1024, 576))

        elif game.level[1] and game.player.rect.x > 900:
            game.level[1] = False
            game.level[2] = True
            for i in game.all_senblue:
                game.delete_senator_blue(i)
            for j in game.all_senred:
                game.delete_senator_red(j)
            channelDoor.play(pygame.mixer.Sound("SoundMusic/Porte.ogg"), 0)

            game.player.rect.x = 20
            game.spawn_senator_red(1)
            game.spawn_senator_blue(2)
            game.spawn_senator_red(1)
            game.spawn_policier(2)
            game.spawn_matraque(2)
            background = pygame.transform.scale(pygame.image.load('asset/hall.jpg'), (1024, 576))

        elif game.level[2] and game.player.rect.x > 900 and game.count_policiers == 0:
            game.level[2] = False
            game.level[3] = True
            for i in game.all_senblue:
                game.delete_senator_blue(i)
            for j in game.all_senred:
                game.delete_senator_red(j)
            channelDoor.play(pygame.mixer.Sound("SoundMusic/Porte.ogg"), 0)

            game.player.rect.x = 20
            game.spawn_senator_red(2)
            game.spawn_senator_blue(2)
            game.spawn_senator_red(3)
            game.spawn_senator_blue(2)
            game.spawn_policier(4)
            game.spawn_matraque(3)



            background = pygame.image.load('asset/chamber.jpg')

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
            if not (police.dead):
                police.move()
                police.randomFire()
            for bullet in police.all_bullets:
                bullet.move(game.player)

        # Policiers bim bam boum
        for police in game.all_matraque:
            police.refresh(screen)
            # do actions
            if not (police.dead):
                police.move()
                police.randomAttack()

        # Senators
        for senablue in game.all_senblue:
            senablue.refresh(screen)
            if not (senablue.dead):
                senablue.move()
                senablue.gravity()

        for senared in game.all_senred:
            senared.refresh(screen)
            if not (senared.dead):
                senared.move()
                senablue.gravity()

        # Jack
        game.player.refresh(screen)

        # Mouvements de Jack
        if not (game.player.dead):
            # JUMP
            if game.pressed.get(pygame.K_UP):
                game.player.jump()
            game.player.gravity()
            # RIGHT
            if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x < 970:
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

    if game.pressed.get(pygame.K_SPACE) and game.playing == False:
        game.playing = True
        background = pygame.image.load('asset/background.png')

        game.spawn_senator_blue(1)
        game.spawn_senator_red(1)
        game.spawn_senator_blue(1)
        game.spawn_matraque(2)


    for event in pygame.event.get():  # event est une liste
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:  # On appuie sur une touche
            game.pressed[event.key] = True  # On reste appuyé sur une touche
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False  # On lache la touche

        elif not game.player.dead and event.type == randomVotebarIncrease:  # on augmente la barre aléatoirement
            rand = random.random()  # nombre entre 0 et 1
            if rand < 0.5:  # 50% d'augmenter les bleus
                hud.votebar.blueInc()
            elif rand < 0.7:  # 20% d'augmenter les rouges
                hud.votebar.redInc()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.playing == False:
            if rectangle.collidepoint(event.pos) :
                game.playing = True
                background = pygame.image.load('asset/background.png')

                game.spawn_senator_blue(1)
                game.spawn_senator_red(1)
                game.spawn_senator_blue(1)
                game.spawn_senator_red(1)
                game.spawn_matraque(2)
