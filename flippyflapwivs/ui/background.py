"""
background.py
Author: Adam Beagle

Purpose:
  Contains Background class.
"""
import pygame

from .sprites import Cloud

class Background:
    """
    Subclasses should add sprites with self-contained update() behavior to
    Background.sprites.
    """
    def __init__(self, fill_color):
        self.fill_color = fill_color
        
    def update(self, gamestate, gamedata, dt):
        if gamestate.state != gamestate.WAIT_RESET:
            self.sprites.update(gamestate, gamedata, dt)

    def draw(self, sfc):
        sfc.fill(self.fill_color)
        self.sprites.draw(sfc)

class BlueSkyBackground(Background):
    def __init__(self):
        super().__init__((135, 206, 235))
        self.sprites = pygame.sprite.Group(
            Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(),
        )


