import pygame
from Jack import Player
from Policier import Policier
class Game:

    def __init__(self, hud):
        # Jack
        self.player = Player(hud)
        # Policiers
        self.all_policiers = pygame.sprite.Group()
        self.spawn_policier()

        self.pressed = {}

    def spawn_policier(self):
        policier = Policier()
        self.all_policiers.add(policier)
