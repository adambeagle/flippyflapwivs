"""
platformer.game

DESCRIPTION:
  This subpackage contains all "pure" game logic, i.e. pygame is not touched.
  The goal is to abstract out as much game logic as possible so the ui is less
  cluttered with logic and more about merely visually representing the current
  state of the game.

COORDINATE SYSTEM:
  The gamedata module assumes a coordinate system where the ranges of both
  the x and y axes are [0, 1], where the extents represent the edges of the
  visible area. It is assumed the positive direction of each mirrors Pygame,
  i.e. the positive direction of x is "right" and that of y is "down."
  All positions, constants, etc. in this subpackage use this
  system. The ui package is expected to translate such values to screen
  coordinates.
"""
from .gamedata import GameData
from .gamestate import GameState
