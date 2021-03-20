import pygame
import random




class Matraque(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 2
        self.max_health = 2
        self.attack = 1
        self.currentSprite = pygame.transform.scale(pygame.image.load('asset/police_def_stick.png'), (160, 160))
        self.rect = self.currentSprite.get_rect()
        self.rect.x = 800
        self.rect.y = 380
        self.velocity = 4
        self.sound = pygame.mixer.Channel(2)

        # bullets
        self.bulletCooldown = 0
        self.all_bullets = pygame.sprite.Group()

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
        self.spriteDeath = pygame.transform.scale(pygame.image.load('asset/police_death.png'), (160, 160))

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

    # visual refresh of policier with animations
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

        # do the actual update (if we have been hit, skip 1 in 2 frames)
        if (self.damagedFrame % 8 < 4):
            screen.blit(self.currentSprite, self.rect)

    def delete_policier(self):
        self.remove()
