"""
util.py
Author: Adam Beagle

PURPOSE:
  Contains helper classes and functions specific to the ui subpackage.
"""

import pygame
from adamlib.exceptions import BaseErrvalException

from flippyflapwivs import CONFIG

# BASE CLASSES
class BaseSurface(pygame.Surface):
    """
    All surfaces used in UI should inherit from this class to match
    UIManager's expected API.
    """
    def __init__(self, size, **kwargs):
        super().__init__(size, **kwargs)
        self.rect = self.get_rect()
    
    def draw(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

class BaseFlapException(BaseErrvalException):
    pass

# FUNCTIONS
def game_coords_to_ui(x=0, y=0):
    """
    Translate game package coordinates (range [0, 1]) to screen coordinates.
    Either or both x and/or y may be passed, but a tuple (x, y) is always
    returned (unpassed coordinate will default to 0).
    """
    w, h = CONFIG.SCREEN_SIZE
    return (w*x, h*y)
