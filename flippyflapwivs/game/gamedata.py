"""
gamedata.py
Author: Adam Beagle

PURPOSE:
  Includes Game class, game object classes Column and Player, and GameData
  class.
  
  GameData exposes minimal needed information about the game data to ui
  update() methods.

USAGE:
  External users should use only a GameData instance. GameData is available
  via the package's __init__.py.
"""
from math import ceil, sin
from time import clock

from adamlib.game.utilclasses import Base2dObject

class Column(Base2dObject):
    """
    Defines a column obstacle. For now, the opening for the player to pass
    through is handled by the UI. update() should be called once per frame
    by the Game instance.

    ATTRIBUTES:
      DX - Change in x per frame at 60fps
      W  - Column width

    INHERITED ATTRIBUTES:
      x, y, pos

    METHODS:
      update
    """
    DX = -0.0047
    W = 0.08 
    
    def __init__(self, startx):
        super().__init__(startx, 0)
    
    def update(self, gamestate, dt):
        gs = gamestate
        if gs.state in gs.MAINGAME:
            self.x = self.x + dt*self.DX

class Player(Base2dObject):
    """
    Defines the player object. Game physics are handled here. update() should
    be called once per frame by the Game instance.

    ATTRIBUTES:
      G      - Gravity constant (per frame at 60fps)
      FLAP   - y velocity on a flap event
      STARTX
      STARTY

    INHERITED ATTRIBUTES:
      x, y, pos

    METHODS:
      update
    """
    G = 0.0007 # Gravity constant
    FLAP = -0.012
    STARTX = 0.15
    STARTY = 0.5
    
    def __init__(self):
        super().__init__(self.STARTX, self.STARTY, miny=0, maxy=1)
        self.score = 0
        self.dy = 0

    def update(self, gamestate, dt):
        gs = gamestate

        if gs.state == gs.WAIT_FIRST_FLAP:
            self.y = self._default_position()
            
        elif gs.state in gs.MAINGAME or gs.state == gs.WAIT_RESET:
            if gs.state == gs.FLAP:
                self.dy = self.FLAP
                
            elif gs.state == gs.WAIT_RESET and self.y >= 1:
                gs.state = gs.RESET

            self.dy += dt*self.G
            self.y += dt*self.dy
            
        if gs.state == gs.RESET:
            self.score = 0
            self.y = self._default_position()

    def _default_position(self):
        return 0.3 + 0.05*sin(3*clock())

class Game:
    """
    ATTRIBUTES:
      column_dist - Distance between columns
      N_COLUMNS   - Max number of columns on screen at any time
    """
    COLUMN_DIST = 0.2
    N_COLUMNS = ceil(1 / (Column.W + COLUMN_DIST))
    
    def __init__(self, high_score=0):
        self.player = Player()
        self.high_score = high_score
        self.reset()

    def reset(self):
        self.columns = []
        for i in range(self.N_COLUMNS):
            self.columns.append(Column(1 + i*(Column.W + self.COLUMN_DIST)))

        self.player.pos = (Player.STARTX, Player.STARTY)

    def postupdate(self, gamestate, dt):
        gs = gamestate
        if gs.state == gs.COLLISION:
            self.player.dy = 1.5*self.player.FLAP

    def update(self, gamestate, dt):
        gs = gamestate
        self.player.update(gamestate, dt)

        if self.player.score > self.high_score:
            self.high_score = self.player.score
        
        for c in self.columns:
            c.update(gamestate, dt)

        if gs.state in gs.MAINGAME:
            for c in self.columns:
                scoremin = c.x
                scoremax = scoremin + abs(dt*c.DX)
                if c.x + c.W < 0:
                    c.x = 1
                elif scoremin <= self.player.x <= scoremax:
                    gs.state = gs.SCORE
                    self.player.score += 1
                    
        elif gs.state == gs.RESET:
            self.reset()

class GameData:
    """
    The interface for main to the game subpackage. Exposes minimal
    information about the current state of the game data to main and ui.

    ATTRIBUTES (all read-only):
      column_positions - Tuple of position tuples
      high_score
      player_position  - Position tuple
      n_columns
      score
      scroll_speed     - See Column.DX
    """
    def __init__(self, high_score):
        self._game = Game(high_score)

    def postupdate(self, gamestate, dt):
        self._game.postupdate(gamestate, dt)

    def update(self, gamestate, dt):
        self._game.update(gamestate, dt)

    @property
    def column_positions(self):
        return tuple(c.pos for c in self._game.columns)

    @property
    def high_score(self):
        return self._game.high_score

    @property
    def player_position(self):
        return self._game.player.pos

    @property
    def n_columns(self):
        return Game.N_COLUMNS

    @property
    def score(self):
        return self._game.player.score

    @property
    def scroll_speed(self):
        return Column.DX

