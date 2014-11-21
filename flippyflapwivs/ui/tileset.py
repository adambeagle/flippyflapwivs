"""
tileset.py
Author: Adam Beagle

USAGE:
    Normal users should import the TILESET object, and use its TILES attribute
    to access individual tile subsurfaces.

    TILESET.init() must be called AFTER pygame.init() and
    pygame.display.set_mode() have been called for TILESET.TILES to be
    correctly instantiated.

    Use the instructions for _tileset_map below to map descriptive names
    to particular tiles.
"""
from adamlib.game.pygame.tileset import tileset_to_dict
import pygame

from .resmaps import IMAGES

class Tileset:
    """
    Wrapper object for tileset constants.
    For use in this module only. Other modules must use the TILESET instance
    of this class.

    init() must be called AFTER pygame.init() and pygame.display.set_mode()
    have been called for TILESET.TILES to be correctly instantiated.
    """
    SIDE = 64
    TILES = None
    tileset_img = None

    def init(self):
        """
        Init _tileset_img and TILES. No return value. This function must be
        called after pygame.init() and pygame.display.set_mode() have been
        called or pygame.error will be raised.
        """
        self.tileset_img = pygame.image.load(IMAGES['tileset']).convert_alpha()
        self.TILES = tileset_to_dict(
            self.tileset_img, self.SIDE, _tileset_map
        )

# Values of map are (x, y) coordinates to TILESET_IMG.
# Sprite pieces are square with side length SIDE, so (0, 0) corresponds to
# top left sprite, (0, 1) corresponds to second sprite in first row, ect.
#
# If a value is a 4-tuple, the final two coordinates are of the bottom left
# sprite. The rect subsurface for the key in this case will be the union
# of the top-right and bottom-left Rects.
_tileset_map = {
    'pc_right'    : (0, 0), # pc = player character
    'pc_foward'  : (1, 0),
    'cloud'       : (2, 0, 3, 0),
    'ground'      : (0, 2),
    'column'      : (2, 2),
    'column_open' : (2, 3),
    '0'           : (0, 4),
    '1'           : (1, 4),
    '2'           : (2, 4),
    '3'           : (3, 4),
    '4'           : (4, 4),
    '5'           : (5, 4),
    '6'           : (6, 4),
    '7'           : (7, 4),
    '8'           : (8, 4),
    '9'           : (9, 4),
}

TILESET = Tileset()
