import pygame
from Jack import Player
from Policier import Policier
from Policier_matraque import Matraque
from Senator import SenatorBlue
from Senator import SenatorRed

class Game:
    def __init__(self, hud):
        # Jack
        self.player = Player(hud, self)
        self.pressed = {}
        self.level = [True, False, False, False, False]

        # Policiers
        self.all_policiers = pygame.sprite.Group()
        self.all_matraque = pygame.sprite.Group()
        self.spawn_matraque()
        self.count_policiers = 1

        # Sénateurs
        self.all_senblue = pygame.sprite.Group()
        self.all_senred = pygame.sprite.Group()
        self.spawn_senator_blue()
        self.count_senator_blue = 1
        self.count_senator_red = 1

    def spawn_policier(self):
        policier = Policier(self)
        self.all_policiers.add(policier)

    def spawn_matraque(self):
        matraque = Matraque(self)
        self.all_matraque.add(matraque)

    def spawn_senator_blue(self):
        senblue = SenatorBlue(self)
        self.all_senblue.add(senblue)

    def spawn_senator_red(self):
        senred = SenatorRed(self)
        self.all_senred.add(senred)
