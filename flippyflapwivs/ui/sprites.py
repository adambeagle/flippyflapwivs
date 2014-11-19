from random import choice, uniform

from adamlib.util.misc import iterdigits
import pygame

from flippyflapwivs import CONFIG
from .tileset import TILESET
from .util import game_coords_to_ui

###############################################################################
# BASE CLASSES
class TilesetSprite(pygame.sprite.DirtySprite):
    """
    Base class for sprites whose image comes from a (currently *the*)
    tileset image.

    The object's 'image' attribute is a subsurface of full tileset image.
    """
    def __init__(self, key, *groups):
        """key is TILESET.TILES key to sprite image."""
        super().__init__(*groups)
        self.image = TILESET.TILES[key]
        self.rect = pygame.Rect((0, 0), self.image.get_size())

###############################################################################
# SPRITES
class Cloud(TilesetSprite):
    """Cloud sprite. Automatically travels left at random speed."""
    def __init__(self, *groups):
        super().__init__('cloud', *groups)
        self.dirty = 2
        self.reset()

        # Randomize start position for stagger effect
        sw = CONFIG.SCREEN_SIZE[0]
        self.rect.left = int(sw*uniform(.1, 1))

    def reset(self):
        sw, sh = CONFIG.SCREEN_SIZE
        self.rect.left = sw
        self.rect.top = int(sw*uniform(.02, .2))
        self.dx = -1*game_coords_to_ui(uniform(.0002, .002))[0]

    def update(self, gamestate, gamedata, dt):
        if self.rect.right <= 0:
            self.reset()

        self.rect.right += dt*self.dx

class Column(pygame.sprite.DirtySprite):
    column_img = None 
    column_open_img = None 
    column_close_img = None 
    
    def __init__(self, *groups):
        super().__init__(*groups)

        # Instantiate images
        self.column_img = TILESET.TILES['column']
        self.column_open_img = TILESET.TILES['column_open']
        self.column_close_img = pygame.transform.flip(
            TILESET.TILES['column_open'], 0, 1
        )
        
        side = TILESET.SIDE
        self.w, self.h = side, CONFIG.SCREEN_SIZE[1] - side
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.left = CONFIG.SCREEN_SIZE[0]
        self.mask = None # Set in _initial_draw
        self.dirty = 0
        self._initial_draw()

    def _initial_draw(self):
        side = TILESET.SIDE
        open_top = int(uniform(.2*self.h, .7*self.h))
        self.image.blit(self.column_open_img, (0, open_top))

        # Blit column above open
        for y in range(open_top - side, (-side) + 1, -side):
            self.image.blit(self.column_img, (0, y))

        # Blit column below open
        self.image.blit(self.column_close_img, (0, open_top + 2*side))
        for y in range(open_top + 3*side, self.h, side):
            self.image.blit(self.column_img, (0, y))

        self.mask = pygame.mask.from_surface(self.image)

    # Columns are updated in level.Level
    def update(self, *args, **kwargs):
        pass

class Ground(pygame.sprite.DirtySprite):
    single_img = None 

    def __init__(self, scroll_speed, *groups):
        super().__init__(*groups)
        if self.single_img is None:
            self.single_img = TILESET.TILES['ground']
        self.speed = scroll_speed
        self.w, self.h = CONFIG.SCREEN_SIZE[0] + TILESET.SIDE, TILESET.SIDE
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.bottom = CONFIG.SCREEN_SIZE[1]
        self.mask = pygame.mask.Mask((self.w, self.h))
        self.mask.fill()
        self._initial_draw()

    def update(self, gamestate, gamedata, dt):
        gs = gamestate

        if self.rect.left >= (-TILESET.SIDE) + dt*self.speed:
            self.rect.left -= dt*self.speed
        else:
            self.rect.left = 0

    def _initial_draw(self):
        for x in range(0, self.rect.w + 1, TILESET.SIDE):
            self.image.blit(self.single_img, (x, 0))

class Score(pygame.sprite.DirtySprite):
    def __init__(self, *groups, score=0, high_score=0):
        super().__init__(*groups)
        side = TILESET.SIDE
        self.image = pygame.Surface((3*side, side), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.top = game_coords_to_ui(y=.02)[1]
        self.rect.right = CONFIG.SCREEN_SIZE[0]
        self._redraw(score)

    def draw(self, sfc):
        sfc.blit(self.image, self.rect.topleft)

    def update(self, gamestate, gamedata, dt):
        if gamestate.state in (gamestate.SCORE, gamestate.RESET):
            self._redraw(gamedata.score)

    def _redraw(self, score):
        self.image.fill((0, 0, 0, 0))
        for i, d in enumerate(iterdigits(score)):
            x = self.rect.width - (i + 1)*TILESET.SIDE

            # Custom offset for this tileset
            x += 20*i
                
            self.image.blit(TILESET.TILES[str(d)], (x, 0))
