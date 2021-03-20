import pygame
from Jack import Player

class Game:

    def __init__(self, screen):

        # Jack
        self.player = Player(screen)
        self.pressed = {}