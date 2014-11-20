"""
background.py
Author: Adam Beagle

PURPOSE:
  Implements background, i.e. visual elements that are not expected to be
  interacted with in any way.
"""
import pygame

from .sprites import Cloud

class Background:
    """
    Base class for backgrounds. Subclasses should add sprites with
    self-contained update() behavior to a `sprites` attribute.
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
    """Simple background with solid blue sky and moving clouds."""
    def __init__(self):
        super().__init__((135, 206, 235))
        self.sprites = pygame.sprite.Group(
            Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(),
        )
