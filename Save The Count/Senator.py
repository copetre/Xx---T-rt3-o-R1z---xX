import pygame
import random

class SenatorBlue(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 1
        self.max_health = 1
        self.velocity = 2
        self.dead = False

        # policier box
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/senator_def_blue.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 800
        self.rect.y = 380
        self.sound = pygame.mixer.Channel(3)

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('asset/senator_def_blue.png'), (160, 160)),
                                pygame.transform.scale(pygame.image.load('asset/senator_walk_blue.png'), (160, 160))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeath = pygame.transform.scale(pygame.image.load('asset/senator_death_blue.png'), (160, 160))

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

    def right(self):
        self.walkAnimationRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
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

    # visual refresh of blue senator with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each

        # set current sprite
        if (self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
        elif (self.walkAnimationRight):
            self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks

        # if we've been damaged, increase damaged frame (same if we are dead)
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 37):  # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if (self.health == 0):
                    self.delete_senator()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_senator(self):
        self.game.all_policiers.remove(self)

class SenatorRed(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        # pygame
        self.game = game

        # attributes
        self.health = 1
        self.max_health = 1
        self.velocity = 2
        self.dead = False

        # policier box
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/senator_def_red.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 800
        self.rect.y = 380
        self.sound = pygame.mixer.Channel(3)

        # IA
        self.newpos = random.randint(5, 924)
        self.newpos -= self.newpos % self.velocity

        # animation déplacement
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkLeft = [pygame.transform.scale(pygame.image.load('asset/senator_def_red.png'), (160, 160)),
                                pygame.transform.scale(pygame.image.load('asset/senator_walk_red.png'), (160, 160))]
        self.spritesWalkRight = [pygame.transform.flip(self.spritesWalkLeft[0], True, False),
                                 pygame.transform.flip(self.spritesWalkLeft[1], True, False)]
        self.walkFrame = 0

        # animation dommage/mort
        self.damaged = False
        self.damagedFrame = 0
        self.spriteDeath = pygame.transform.scale(pygame.image.load('asset/senator_death_red.png'), (160, 160))

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

    def right(self):
        self.walkAnimationRight = True
        self.rect.x += self.velocity

    def left(self):
        self.walkAnimationLeft = True
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

    # visual refresh of blue senator with animations
    def refresh(self, screen):
        # if walking in any direction, increase frame
        if (self.walkAnimationLeft or self.walkAnimationRight):
            self.walkFrame = (self.walkFrame + 1) % 12  # %12 because we have 2 frames * 6 ticks each

        # set current sprite
        if (self.walkAnimationLeft):
            self.currentSprite = self.spritesWalkLeft[self.walkFrame // 6]  # //6 because update every 6 ticks
        elif (self.walkAnimationRight):
            self.currentSprite = self.spritesWalkRight[self.walkFrame // 6]  # //6 because update every 6 ticks

        # if we've been damaged, increase damaged frame (same if we are dead)
        if (self.damaged):
            self.damagedFrame += 1
            if (self.damaged and self.damagedFrame == 37):  # stop animation
                self.damaged = False
                self.damagedFrame = 0
                if (self.health == 0):
                    self.delete_senator()

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_senator(self):
        self.game.all_policiers.remove(self)