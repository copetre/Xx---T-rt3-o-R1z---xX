import pygame
import random
import time
from scripts import * # our entities & stuff

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
# First Windows

pygame.display.set_caption("CAPITOL CONQUEST")
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()

running = True  # Game Running

background = pygame.image.load('assets/FIRST_SCREEN_1.png')
firstsreen = [pygame.image.load('assets/FIRST_SCREEN_1.png'), pygame.image.load('assets/FIRST_SCREEN_2.png'),
              pygame.image.load('assets/FIRST_SCREEN_3.png'), pygame.image.load('assets/FIRST_SCREEN_2.png'), ]
levels = [pygame.image.load('assets/voting.jpg'), pygame.image.load('assets/street.jpg'),pygame.image.load('assets/exterior.jpg'),
          pygame.image.load('assets/hall.jpg'), pygame.image.load('assets/chamber.jpg'), ]
frame = 0

hud = HUD()

# Create characters
game = Game(hud)
arrowLeft = pygame.transform.scale(pygame.image.load('assets/arrow.png'), (200, 100))
arrowRight = pygame.transform.flip(arrowLeft, True, False)
sanders = pygame.transform.scale(pygame.image.load('assets/bernie_sitting_mitten.png'), (350, 350))

# Every O.5 secs, change VoteBar
randomVotebarIncrease = pygame.USEREVENT + 1
pygame.time.set_timer(randomVotebarIncrease, 500)

# Sound Bank
channelFond = pygame.mixer.Channel(1)
channelDoor = pygame.mixer.Channel(7)
soundNiveauBureauVotes2 = pygame.mixer.Sound('sounds/NiveauBureauVotes2.mp3.ogg')
soundPorte = pygame.mixer.Sound("sounds/Porte.ogg")
soundPartiePerdue = pygame.mixer.Sound("sounds/PartiePerdue.ogg")
soundNiveauCapitol = pygame.mixer.Sound('sounds/NiveauCapitol.ogg')
soundJeuFini = pygame.mixer.Sound("sounds/JeuFini.ogg")

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
        screen.blit(sanders, (350, 100))

    # If Alive
    if game.playing and game.player.health == 0:
        game.gameOverFrame += 1
        if (game.gameOverFrame == 120):  # After 2 seconds, back to menu
            game.playing = False
            hud = HUD()
            game = Game(hud)

    elif game.win:
        game.gameOverFrame += 1
        if game.gameOverFrame == 1200:  # After 10 seconds, back to menu
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
            
            background = pygame.image.load('assets/GAME OVER.jpg')
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
        if (game.gameOverFrame == 540):  # After 9 sec, back to menu
            game.playing = False
            hud = HUD()
            game = Game(hud)

    # Actual level
    if not game.playing and not game.win:
        frame = (frame + 1) % 24  # %12 because we have 2 frames * 6 ticks each
        background = firstsreen[frame // 6]
    else:
        if game.level[0] and game.count_policiers == 0:

            if game.count_manifestants == 0:
                game.spawn_manifestants(7)

            if game.player.rect.x > 900 and game.count_policiers == 0:
                game.level[0] = False
                game.level[1] = True

                background = niveau(levels[1], 2, 0, 0, 0)
                for i in game.all_senblue:
                    game.delete_senator_blue(i)
                for j in game.all_senred:
                    game.delete_senator_red(j)
                for k in game.all_manifestants:
                    game.delete_manifestant(k)
                game.spawn_manifestants(3)


        elif game.level[1] and game.count_policiers == 0: # Street
            if game.player.rect.x > 900:
                game.level[1] = False
                game.level[2] = True
                game.gotRoomHealAlready = False
                background = niveau(levels[2], 1, 1, 1, 1)

        elif game.level[2] and game.count_policiers == 0: # Front congress
            if game.count_manifestants == 0:
                game.spawn_manifestants(7)
            if game.player.rect.x > 900:
                game.level[2] = False
                game.level[3] = True
                game.gotRoomHealAlready = False
                channelDoor.play(soundPorte, 0)

                game.player.rect.x = 20
                background = niveau(levels[3], 2, 1, 2, 2)

        elif game.level[3] and game.count_policiers == 0: # Hall
            if game.count_manifestants == 0:
                game.spawn_manifestants(7)
            if game.player.rect.x > 900:
                channelFond.play(soundNiveauCapitol, -1)
                game.level[3] = False
                game.level[4] = True
                game.gotRoomHealAlready = False
                channelDoor.play(soundPorte, 0)

                game.player.rect.x = 20
                background = niveau(levels[4], 1, 1, 5, 3)
        elif game.level[4]: # Chamber
            if random.random() < 0.01:
                game.spawn_senator_blue(1)

            #Trump screen
            if game.playing and hud.votebar.redPercent > 50 and game.player.rect.x > 900 and game.count_policiers == 0:
                game.win = True
                game.level[4] = False
                game.level[5] = True
                game.gotRoomHealAlready = False
                background = pygame.image.load('assets/WIN.jpg')
                channelFond.play(soundJeuFini, 0)
                game.spawn_senator_red(15)
                game.spawn_manifestants(15)
                game.spawn_senator_blue(7)
                game.player.rect.x = 20
            # Sanders screen
            elif game.playing and hud.votebar.redPercent > 50 and game.player.rect.x < 20 and game.count_policiers == 0:
                
                game.level[4] = False
                game.level[6] = True
                game.gotRoomHealAlready = False
                background = pygame.image.load('assets/hall.jpg')
                channelFond.play(soundJeuFini, 0)
                game.spawn_senator_blue(15)
                game.player.rect.x = 900
        elif game.level[6] == True and game.player.rect.x < 20 : #Sanders to Trump
            for i in game.all_senblue:
                game.delete_senator_blue(i)
            game.win = True
            game.level[6] = False
            game.level[5] = True
            background = pygame.image.load('assets/WIN.jpg')
            channelFond.play(soundJeuFini, 0)
            game.spawn_senator_red(15)
            game.spawn_manifestants(15)




        # If all ennemies killed, the votBar is faster
        if(game.level[4] and game.count_policiers == 0 and not(game.increaseRedOdds)):
            game.increaseRedOdds = True
            pygame.time.set_timer(randomVotebarIncrease, 0)
            pygame.time.set_timer(randomVotebarIncrease, 250)

        # Arrow if all cops are deads
        if (game.level[6]) :
            screen.blit(arrowRight, (25, 200))
            
        elif (game.count_policiers == 0 and game.level[4] == False
            and game.win == False and game.lose == False):
            screen.blit(arrowLeft, (800, 200))
        # Last room = win
        elif (game.level[4] and hud.votebar.redPercent > 50):
            screen.blit(arrowLeft, (800, 200))
            screen.blit(arrowRight, (25, 200))
        elif (game.level[6]) :
            screen.blit(arrowRight, (25, 200))


        if not(game.gotRoomHealAlready) and game.count_senator_blue == 0:
            game.gotRoomHealAlready = True
            game.player.heal_Jack()

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

        # Cops pan pan
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

        # Cops bim bam boum
        for police in game.all_matraque:
            police.refresh(screen)
            # do actions
            if not (police.dead):
                police.move()
                police.randomAttack()



        # Jack
        game.player.refresh(screen)

        # Mouvements of Jack
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
        background = niveau(levels[0],0,1,1,0)
        game.gotRoomHealAlready = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:  # Press key
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False  # key up

        # Randomly grow the vote bar
        elif not game.player.dead and event.type == randomVotebarIncrease and not game.win:
            rand = random.random()  # 0 < x < 1

            if not(game.increaseRedOdds):
                if rand < 0.7:  # 70% for blue
                    hud.votebar.blueInc()
                else:  # 30% red
                    hud.votebar.redInc()
            else:
                if rand < 0.5 and hud.votebar.bluePercent<50:
                    hud.votebar.blueInc()
                else:
                    hud.votebar.redInc()

        elif event.type == pygame.MOUSEBUTTONDOWN and game.playing == False:
            if rectangle.collidepoint(event.pos):
                channelFond.play(soundNiveauBureauVotes2, -1)
                game.playing = True
                hud.votebar.redPercent = 5
                hud.votebar.bluePercent = 5
                channelDoor.play(soundPorte, 0)

                background = niveau(levels[0], 0, 1, 1, 0)
                game.gotRoomHealAlready = False
