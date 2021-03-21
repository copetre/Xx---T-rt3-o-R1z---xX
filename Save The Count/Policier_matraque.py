import pygame
import random




class Matraque(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 2
        self.max_health = 2
        self.velocity = 4
        self.dead = False

        # policier box
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/police_def_stick.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 800
        self.rect.y = 380
        self.sound = pygame.mixer.Channel(2)
        self.facingRight = False

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('asset/police_def_stick.png'), (160, 160)),
                                pygame.transform.scale(pygame.image.load('asset/police_walk_stick.png'), (160, 160))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeath = pygame.transform.scale(pygame.image.load('asset/police_death_stick.png'), (160, 160))

        # animation attaque
        self.attacking = False
        self.attackFrame = 0
        self.spritesAttackLeft = [pygame.transform.scale(pygame.image.load('asset/police_attack1_stick.png'), (160, 160)),
                                  pygame.transform.scale(pygame.image.load('asset/police_attack2_stick.png'), (160, 160)),
                                  pygame.transform.scale(pygame.image.load('asset/police_attack1_stick.png'), (160, 160)),
                                  pygame.transform.scale(pygame.image.load('asset/police_def_stick.png'), (160, 160))]
        self.spritesAttackRight = [pygame.transform.flip(self.spritesAttackLeft[0], True, False),
                                   pygame.transform.flip(self.spritesAttackLeft[1], True, False),
                                   pygame.transform.flip(self.spritesAttackLeft[2], True, False),
                                   pygame.transform.flip(self.spritesAttackLeft[3], True, False)]

    def move(self):
        if self.newpos > self.rect.x:
            self.right()
        elif self.newpos < self.rect.x:
            self.left()
        else:
            self.newpos = random.randint(5, 924)
            self.newpos -= self.newpos % self.velocity
            self.walkAnimationRight = False
            self.walkAnimationLeft = False

    def randomAttack(self):
        if not(self.attacking):
            if(random.random()<0.025):
                self.attacking = True

    def attack(self):
        if (self.facingRight):
            if (self.rect.x < self.game.player.rect.x < self.rect.x + 160  # horizontal hitbox
                    and self.rect.y >= self.game.player.rect.y - 80):  # vertical hitbox)
                self.game.player.damage()
        else:
            if (self.rect.x > self.game.player.rect.x > self.rect.x - 160  # horizontal hitbox
                    and self.rect.y >= self.game.player.rect.y - 80):  # vertical hitbox)
                self.game.player.damage()

    def right(self):
        self.walkAnimationRight = True
        self.facingRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
        self.facingRight = False
        self.rect.x -= self.velocity

    def damage(self):
        if (self.health > 0):
            self.health -= 1
            self.damaged = True
        if (self.health == 0):
            self.dead = True
            self.walkAnimationRight = False
            self.walkAnimationLeft = False
            self.currentSprite = self.spriteDeath

    # visual refresh of policier with animations
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

        # if we've been damaged, increase damaged frame (same if we are dead)
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 37):  # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if (self.health == 0):
                    self.delete_policier()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_policier(self):
        self.game.all_matraque.remove(self)
        self.game.count_policiers -= 1

