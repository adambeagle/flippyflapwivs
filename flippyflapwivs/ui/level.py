"""
level.py
Author: Adam Beagle
"""
import pygame

from .util import BaseSurface, game_coords_to_ui
from .sprites import Ground, Column

class Level(BaseSurface):
    """
    Wrapper object for level sprites, i.e. ground and columns.
    UiManager should call update() and draw() on every frame.
    """
    def __init__(self, n_columns, scroll_speed):
        self.sprites = pygame.sprite.Group()
        self._speed = scroll_speed
        self.columns = [None]*n_columns
        self._reset_columns()

        Ground(scroll_speed, self.sprites)

    def update(self, gamestate, gamedata, dt):
        gs = gamestate

        # Don't update if WAIT_RESET (nothing in level should change)
        if gs.state == gs.WAIT_RESET:
            return
        
        self.sprites.update(gs, gamedata, dt)
        edge = game_coords_to_ui(1)[0]

        if gs.state == gamestate.RESET:
            self._reset_columns()

        # Update each column's position based on gamedata.column_positions,
        # or spawn a new column if it has gone offscreen
        for i, (c, cp) in enumerate(
            zip(self.columns, gamedata.column_positions)
        ):
            x, y = game_coords_to_ui(*cp)

            if x < edge and c is not None:
                c.rect.topleft = (x, y)
            elif edge <= x <= edge + dt*self._speed:
                self._spawn_column(i)

    def draw(self, sfc):
        self.sprites.draw(sfc)

    def _reset_columns(self):
        for c in self.columns:
            if c is not None:
                c.kill()
            
        self.columns = [None]*len(self.columns)
        self._spawn_column(0)

    def _spawn_column(self, i):
        old_c = self.columns[i]
        if old_c is not None:
            old_c.kill()
            
        c = Column(self.sprites)
        c.rect.x = game_coords_to_ui(1)[0]
        self.columns[i] = c
        return c
