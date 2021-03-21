import pygame
import random
import time
from Game import Game
from HUD import HUD
from Jack import Player

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
# Fenêtre de base

pygame.display.set_caption("CAPITOL CONQUEST")
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

running = True  # Jeu en cours

background = pygame.image.load('asset/FIRST_SCREEN_1.png')
firstsreen = [pygame.image.load('asset/FIRST_SCREEN_1.png'), pygame.image.load('asset/FIRST_SCREEN_2.png'),
              pygame.image.load('asset/FIRST_SCREEN_3.png'), pygame.image.load('asset/FIRST_SCREEN_2.png'), ]
levels = [pygame.image.load('asset/voting.jpg'), pygame.image.load('asset/street.jpg'),pygame.image.load('asset/exterior.jpg'),
          pygame.image.load('asset/hall.jpg'), pygame.image.load('asset/chamber.jpg'), ]
frame = 0

hud = HUD()

# Création des personnages
game = Game(hud)
arrowLeft = pygame.transform.scale(pygame.image.load('asset/arrow.png'), (200, 100))
arrowRight = pygame.transform.flip(arrowLeft, True, False)
sanders = pygame.transform.scale(pygame.image.load('asset/bernie_sitting_mitten.png'), (350, 350))

# toutes les 0.5 seconde, on augmente aléatoirement la barre
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 500)

# Sound Bank
channelFond = pygame.mixer.Channel(1)
channelDoor = pygame.mixer.Channel(7)
soundNiveauBureauVotes2 = pygame.mixer.Sound('SoundMusic/NiveauBureauVotes2.mp3.ogg')
soundPorte = pygame.mixer.Sound("SoundMusic/Porte.ogg")
soundPartiePerdue = pygame.mixer.Sound("SoundMusic/PartiePerdue.ogg")
soundNiveauCapitol = pygame.mixer.Sound('SoundMusic/NiveauCapitol.ogg')
soundJeuFini = pygame.mixer.Sound("SoundMusic/JeuFini.ogg")

# Sound at first
channelFond.play(soundNiveauBureauVotes2, -1)

surface = pygame.Surface((800, 90))
surface.fill((128, 128, 128))
rectangle = surface.get_rect(left=100, top=420)  # alternative = (center = (608, 32))
frame = 0


def niveau(fond, nb_pol, nb_mat, nb_blue, nb_red):  # background, nbre policier, nbre matraque, nbre bleus, nbre rouges
    game.count_senator_blue = 0
    for i in game.all_senblue:
        game.delete_senator_blue(i)
    for j in game.all_senred:
        game.delete_senator_red(j)
    for k in game.all_manifestants:
        game.delete_manifestant(k)

    channelDoor.play(soundPorte, 0)
    game.player.rect.x = 0
    game.spawn_senator_red(nb_red)
    game.spawn_senator_blue(nb_blue)
    game.spawn_policier(nb_pol)
    game.spawn_matraque(nb_mat)
    background = pygame.transform.scale(fond, (1024, 576))
    return background


while running:
    clock.tick(60)

    screen.blit(background, (0, 0))

    
    if game.level[6] == True :
        screen.blit(sanders, (350, 75))

    # Regarde si vivant
    if game.playing and game.player.health == 0:
        game.gameOverFrame += 1
        if (game.gameOverFrame == 120):  # après 2 secondes de mort, retour au menu
            game.playing = False

    elif game.win:

        game.gameOverFrame += 1
        if game.gameOverFrame == 1200:  # après 10 secondes du tableau de Win, retour au menu
            game.playing = False
            game.win = False
            hud = HUD()
            game = Game(hud)

    elif (game.playing and hud.votebar.bluePercent > 50):
        if game.gameOverFrame == 0:

            game.lose = True
            game.level[5] = False
            game.level[4] = False
            game.level[3] = False
            game.level[2] = False
            game.level[1] = False
            game.level[0] = False
            
            background = pygame.image.load('asset/GAME OVER.jpg')
            channelFond.play(soundPartiePerdue, 0)
            for i in game.all_senblue:
                game.delete_senator_blue(i)
            for j in game.all_senred:
                game.delete_senator_red(j)
            for k in game.all_matraque:
                game.delete_matraque(k)
            for l in game.all_matraque:
                game.delete_policier(l)
            for k in game.all_manifestants:
                game.delete_manifestant(k)
            game.player.dead = True
        game.gameOverFrame += 1
        if (game.gameOverFrame == 540):  # après 9 secondes de mort, retour au menu
            game.playing = False
            hud = HUD()
            game = Game(hud)

    # On regarde dans quel niveau on se situe
    if not game.playing and not game.win:
        frame = (frame + 1) % 24  # %12 because we have 2 frames * 6 ticks each
        background = firstsreen[frame // 6]
    else:
        if game.level[0] and game.count_policiers == 0: # Bureau de vote

            if game.count_manifestants == 0:
                game.spawn_manifestants(7)

            if game.player.rect.x > 900 and game.count_policiers == 0:
                game.level[0] = False
                game.level[1] = True
                background = niveau(levels[1], 1, 1, 0, 2)
                for i in game.all_senblue:
                    game.delete_senator_blue(i)
                for j in game.all_senred:
                    game.delete_senator_red(j)
                for k in game.all_manifestants:
                    game.delete_manifestant(k)
                game.spawn_manifestants(3)


        elif game.level[1] and game.count_policiers == 0: # Rue
            if game.player.rect.x > 900:
                game.level[1] = False
                game.level[2] = True
                game.count_senator_blue = 0
                background = niveau(levels[2], 1, 1, 0, 2)
                for i in game.all_senblue:
                    game.delete_senator_blue(i)
                for j in game.all_senred:
                    game.delete_senator_red(j)
                for k in game.all_manifestants:
                    game.delete_manifestant(k)

        elif game.level[2] and game.count_policiers == 0: # Devant congrès
            if game.count_manifestants == 0:
                game.spawn_manifestants(7)
            if game.player.rect.x > 900:
                channelFond.play(soundNiveauCapitol, -1)
                game.level[2] = False
                game.level[3] = True
                for i in game.all_senblue:
                    game.delete_senator_blue(i)
                for j in game.all_senred:
                    game.delete_senator_red(j)
                for k in game.all_manifestants:
                    game.delete_manifestant(k)
                channelDoor.play(soundPorte, 0)

                game.player.rect.x = 20
                background = niveau(levels[3], 2, 3, 3, 3)

        elif game.level[3] and game.count_policiers == 0: # Hall
            if game.count_manifestants == 0:
                game.spawn_manifestants(7)
            if game.player.rect.x > 900:
                channelFond.play(soundNiveauCapitol, -1)
                game.level[3] = False
                game.level[4] = True
                for i in game.all_senblue:
                    game.delete_senator_blue(i)
                for j in game.all_senred:
                    game.delete_senator_red(j)
                for k in game.all_manifestants:
                    game.delete_manifestant(k)
                channelDoor.play(soundPorte, 0)

                game.player.rect.x = 20
                background = niveau(levels[4], 2, 3, 3, 3)
        elif game.level[4]: # Chamber
            if random.random() < 0.005:
                game.spawn_senator_blue(1)

            if game.playing and hud.votebar.redPercent > 50 and game.player.rect.x > 900 and game.count_policiers == 0:
                game.win = True
                game.level[4] = False
                game.level[5] = True
                background = pygame.image.load('asset/WIN.jpg')
                channelFond.play(soundJeuFini, 0)
                game.spawn_senator_red(15)
                game.spawn_manifestants(15)
                game.spawn_senator_blue(7)
            elif game.playing and hud.votebar.redPercent > 50 and game.player.rect.x < 20 and game.count_policiers == 0:
                game.win = True
                game.level[4] = False
                game.level[6] = True
                background = pygame.image.load('asset/hall.jpg')
                channelFond.play(soundJeuFini, 0)
                game.spawn_senator_blue(20)

        # Si on a tué tout le monde et qu'on attend juste la barre, on augmente les votes rouges et la fréquence
        if(game.level[3] and game.count_policiers == 0 and not(game.increaseRedOdds)):
            game.increaseRedOdds = True
            pygame.time.set_timer(randomVotebarIncrease, 0)
            pygame.time.set_timer(randomVotebarIncrease, 250)

        # Flèche si tout le monde est mort
        if (game.count_policiers == 0 and game.level[4] == False
            and game.win == False and game.lose == False):
            screen.blit(arrowLeft, (800, 200))
        # ou si on est dans la dernière salle et qu'on a gagné
        elif (game.level[4] and hud.votebar.redPercent > 50):
            screen.blit(arrowLeft, (800, 200))
            screen.blit(arrowRight, (25, 200))

        if game.count_senator_blue == 0:
            game.player.heal_Jack()
            game.count_senator_blue = -1

        # HUD
        hud.refresh(screen)

        # Manifestants
        for man in game.all_manifestants:
            man.refresh(screen)
            man.move()

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
                senared.gravity()

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
        hud.votebar.redPercent = 5
        hud.votebar.bluePercent = 5
        channelFond.play(soundNiveauBureauVotes2, -1)
        background = niveau(levels[0],0,1,1,1)

    for event in pygame.event.get():  # event est une liste
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:  # On appuie sur une touche
            game.pressed[event.key] = True  # On reste appuyé sur une touche
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False  # On lache la touche

        # on augmente la barre aléatoirement
        elif not game.player.dead and event.type == randomVotebarIncrease and not game.win:
            rand = random.random()  # nombre entre 0 et 1

            if not(game.increaseRedOdds):
                if rand < 0.7:  # 70% d'augmenter les bleus
                    hud.votebar.blueInc()
                else:  # 30% d'augmenter les rouges
                    hud.votebar.redInc()
            else:
                if rand < 0.5 and hud.votebar.bluePercent<50:  # 50% d'augmenter les bleus (mais on les empêche de gagner)
                    hud.votebar.blueInc()
                else:  # 50% d'augmenter les rouges
                    hud.votebar.redInc()

        elif event.type == pygame.MOUSEBUTTONDOWN and game.playing == False:
            if rectangle.collidepoint(event.pos):
                channelFond.play(soundNiveauBureauVotes2, -1)
                game.playing = True
                hud.votebar.redPercent = 5
                hud.votebar.bluePercent = 5
                channelDoor.play(soundPorte, 0)

                background = niveau(levels[0], 0, 1, 1, 1)
