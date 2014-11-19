"""
player.py
Author: Adam Beagle
"""
import pygame

from .tileset import TILESET
from .util import game_coords_to_ui
    
class Wivs(pygame.sprite.DirtySprite):
    """Player sprite. Call update() and draw() once per frame."""
    images = {
        'default' : 'pc_right',
        'collision' : 'pc_foward',
    }

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self._get_image('default')
        self.rect = self.image.get_rect()
        self.dirty = 2

    def draw(self, sfc):
        sfc.blit(self.image, self.rect)

    def update(self, gamestate, gamedata, dt):
        gs = gamestate
        self.rect.topleft = game_coords_to_ui(*gamedata.player_position)

        if gs.state == gs.COLLISION:
            self.image = self._get_image('collision')
        elif gs.state == gs.RESET:
            self.image = self._get_image('default')

    def _get_image(self, key):
        return TILESET.TILES[self.images[key]]
