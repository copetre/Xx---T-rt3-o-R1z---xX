import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, hud, game):
        super().__init__()
        # pygame
        self.hud = hud
        self.game = game

        # attributes
        self.health = 3
        self.max_health = 3
        self.velocity = 4
        self.dead = False

        # player box
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 50
        self.rect.y = 380
        self.facingRight = True

        # Sound
        self.sound = pygame.mixer.Channel(0)

        # jump
        self.jumping = False
        self.jumpingVelocity = 0

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkRight = [pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160)),
                                 pygame.transform.scale(pygame.image.load('asset/jake_walk.png'), (160, 160))]
        self.spritesWalkLeft = [pygame.transform.flip(self.spritesWalkRight[0], True, False),
                                pygame.transform.flip(self.spritesWalkRight[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeathRight = pygame.transform.scale(pygame.image.load('asset/jake_death.png'), (160, 160))
        self.spriteDeathLeft = pygame.transform.flip(self.spriteDeathRight, True, False)

        # animation attaque
        self.attacking = False
        self.attackFrame = 0
        self.spritesAttackRight = [pygame.transform.scale(pygame.image.load('asset/jake_attack1.png'), (160, 160)),
                                   pygame.transform.scale(pygame.image.load('asset/jake_attack2.png'), (160, 160)),
                                   pygame.transform.scale(pygame.image.load('asset/jake_attack1.png'), (160, 160)),
                                   pygame.transform.scale(pygame.image.load('asset/jake_def.png'), (160, 160))]
        self.spritesAttackLeft = [pygame.transform.flip(self.spritesAttackRight[0], True, False),
                                  pygame.transform.flip(self.spritesAttackRight[1], True, False),
                                  pygame.transform.flip(self.spritesAttackRight[2], True, False),
                                  pygame.transform.flip(self.spritesAttackRight[3], True, False)]

    def right(self):
        if self.sound.get_busy() == False:
            self.sound.play(pygame.mixer.Sound('SoundMusic/MarcheJack.ogg'), 1)
        self.walkAnimationRight = True
        self.facingRight = True
        self.rect.x += self.velocity

    def left(self):
        if self.sound.get_busy() == False:
            self.sound.play(pygame.mixer.Sound('SoundMusic/MarcheJack.ogg'), 1)
        self.walkAnimationLeft = True
        self.facingRight = False
        self.rect.x -= self.velocity

    def jump(self):
        # only jumps if on ground
        if (self.rect.y == 380):
            self.jumping = True
            self.jumpingVelocity = 12
            self.sound.play(pygame.mixer.Sound('SoundMusic/JackSaut.ogg'), 0)

    def gravity(self):
        # if we are jumping, continue going upwards
        if (self.jumping):
            # move upwards
            self.rect.y = min(self.rect.y - self.jumpingVelocity,380)

            # decrease y-velocity
            self.jumpingVelocity = self.jumpingVelocity - 0.5 
            
            if (self.rect.y == 380):
                #if on the ground, stop
                self.jumping = False
                self.jumpingVelocity = 0

    def damage(self):
        if (self.health > 0):
            self.sound.play(pygame.mixer.Sound('SoundMusic/JackAttaqué.ogg'), 0)
            self.health -= 1
            self.hud.loseHeart()
            self.damaged = True
        if (self.health == 0):
            self.dead = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False

    def launchAttack(self):
        self.attacking = True

    def attack(self):
        if (self.facingRight):
            for police in self.game.all_policiers:
                if (self.rect.x < police.rect.x < self.rect.x + 160  # horizontal hitbox
                        and self.rect.y + 80 > police.rect.y):  # vertical hitbox)
                    police.damage()
                    self.scareSenators()
            for police in self.game.all_matraque:
                if (self.rect.x < police.rect.x < self.rect.x + 160  # horizontal hitbox
                        and self.rect.y + 80 > police.rect.y):  # vertical hitbox)
                    police.damage()
                    self.scareSenators()
            for senator in self.game.all_senblue:
                if (self.rect.x < senator.rect.x < self.rect.x + 160  # horizontal hitbox
                        and self.rect.y + 80 > senator.rect.y):  # vertical hitbox)
                    senator.damage()
                    self.scareSenators()
            for senator in self.game.all_senred:
                if (self.rect.x < senator.rect.x < self.rect.x + 160  # horizontal hitbox
                        and self.rect.y + 80 > senator.rect.y):  # vertical hitbox)
                    senator.damage()
                    self.scareSenators()
        else:
            for police in self.game.all_policiers:
                if (self.rect.x > police.rect.x > self.rect.x - 160  # horizontal hitbox
                        and self.rect.y + 80 > police.rect.y):  # vertical hitbox)
                    police.damage()
                    self.scareSenators()
            for police in self.game.all_matraque:
                if (self.rect.x > police.rect.x > self.rect.x - 160  # horizontal hitbox
                        and self.rect.y + 80 > police.rect.y):  # vertical hitbox)
                    police.damage()
                    self.scareSenators()
            for senator in self.game.all_senblue:
                if (self.rect.x > senator.rect.x > self.rect.x - 160  # horizontal hitbox
                        and self.rect.y + 80 > senator.rect.y):  # vertical hitbox)
                    senator.damage()
                    self.scareSenators()
            for senator in self.game.all_senred:
                if (self.rect.x > senator.rect.x > self.rect.x - 160  # horizontal hitbox
                        and self.rect.y + 80 > senator.rect.y):  # vertical hitbox)
                    senator.damage()
                    self.scareSenators()
    
    def scareSenators(self):
        for senator in self.game.all_senblue:
            senator.scared = True
            senator.velocity = 3
        for senator in self.game.all_senred:
            senator.scared = True
            senator.velocity = 3

    # visual refresh of Jack with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each
        # if attacking, increase frame
        if (self.attacking):
            self.attackFrame = (self.attackFrame + 1)
            if (self.attackFrame == 6):  # call the attack function on 2nd frame of animation
                self.attack()
            if (self.attackFrame >= 24):  # %24 because we have 4 frames * 6 ticks each
                self.attacking = False
                self.attackFrame = 0

        # set current sprite
        if (self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
        elif (self.walkAnimationRight):
            self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks

        # apply attack animation
        if (self.attacking and not (self.facingRight)):
            self.currentSprite = self.spritesAttackLeft[self.attackFrame // 6]  # //6 because update every 6 ticks
        elif (self.attacking and self.facingRight):
            self.currentSprite = self.spritesAttackRight[self.attackFrame // 6]  # //6 because update every 6 ticks

        # set sprite to dead + blinking
        if(self.dead):
            self.damagedFrame += 1
            if(self.facingRight):
                self.currentSprite = self.spriteDeathRight
            else:
                self.currentSprite = self.spriteDeathLeft

        # if we've been damaged, increase damaged frame for blinking
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 36):  # stop animation
                self.damaged = False
                self.damagedFrame = 0

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)
