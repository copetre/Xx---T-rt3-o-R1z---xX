import pygame
from Jack import Player
from Policier import Policier
from Policier_matraque import Matraque
class Game:

    def __init__(self, hud):
        # Jack
        self.player = Player(hud)
        # Policiers
        self.all_policiers = pygame.sprite.Group()
        self.all_matraque = pygame.sprite.Group()
        self.spawn_policier()
        self.spawn_matraque()
        self.pressed = {}
        self.level = [True, False, False, False, False]

    def spawn_policier(self):
        policier = Policier()
        self.all_policiers.add(policier)

    def spawn_matraque(self):
        matraque = Matraque()
        self.all_matraque.add(matraque)
