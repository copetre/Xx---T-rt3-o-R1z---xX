import pygame

class HUD:
    # screen = the pygame screen to draw on
    def __init__(self, screen):
        # HUD surface
        self.surface = pygame.Surface((1024, 64))
        self.surface.fill((128, 128, 128))
        self.background = self.surface.get_rect()
        screen.blit(self.surface, self.background)

        # Hearts
        self.hearts = []
        for i in range(3):
            self.hearts.append(Heart(screen, i))

class Heart:
    # screen = the pygame screen to draw on
    # index = indicates which heart it is (0, 1, 2)
    def __init__(self, screen, index):
        # attributes
        self.index = index

        # heart surface
        self.surface = pygame.Surface((32, 32))
        self.surface.fill((255, 128, 128))
        self.background = self.surface.get_rect(center = (48 * (self.index+1) - 16, 32))
        screen.blit(self.surface, self.background)