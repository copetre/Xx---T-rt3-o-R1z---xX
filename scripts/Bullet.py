import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, policier, movingLeft):
        super().__init__()
        self.policier = policier
        self.velocity = 5
        self.health = 1
        self.max_health = 1
        self.image = pygame.transform.scale(pygame.image.load('assets/Bullet.png'), (20, 10))
        self.rect = self.image.get_rect()
        if movingLeft:
            self.rect.x = policier.rect.x-25
        else:
            self.rect.x = policier.rect.x+110
        self.rect.y = 461
        self.velocity = 6
        self.movingLeft = movingLeft # true=left, false=right

    def move(self, player):
        if self.movingLeft:
            self.rect.x -= self.velocity
        else:
            self.rect.x += self.velocity

        if(player.rect.x < self.rect.x < player.rect.x+140  # horizontal hitbox
            and self.rect.y<player.rect.y+160): # vertical hitbox
            player.damage()
            self.policier.all_bullets.remove(self) # delete bullet