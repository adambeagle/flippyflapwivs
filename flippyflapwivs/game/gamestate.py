"""
gamestate.py
Author: Adam Beagle

PURPOSE:
  Contains GameState class, which defines and handles sets and
  transitions of game state. See docs of adamlib.game.gamestate for more.

USAGE:
  Main should instantiate a single GameState object for use throughout all
  modules prior to the game loop, and call transition_state once per frame.

  Example state sets:
    # One way
    gs = GameState()
    gs.state = gs.STATE1
    gs.kwargs['some_arg'] = 'something'

    # Another way
    gs.set(gs.STATE1, some_arg='something')
    
"""
import pygame
from adamlib.game.gamestate import GameState as BaseGameState

class GameState(BaseGameState):
    """
    GameState for FlippyFlapWivs.

    See docs/state_flow.png for visual representation of state flow.
    See adamlib.game.gamestate docstrings for base class details.
    """
    def __init__(self):
        states = (
            'WAIT_FIRST_FLAP',
            'DEFAULT',
            'FLAP',
            'SCORE',
            'COLLISION',
            'WAIT_RESET',
            'RESET',
            'PAUSE',
            'QUIT',
        )

        super().__init__(*states)
        self.state = self.WAIT_FIRST_FLAP

        # Define ranges
        self.MAINGAME = tuple(range(self.DEFAULT, self.COLLISION + 1))
        self.NOMOVE = (self.COLLISION, self.WAIT_RESET)

    def transition_state(self):
        """
        All immediate transitions (i.e. always happen on the next
        frame) should occur here.
        """
        if self.state in (self.FLAP, self.SCORE):
            self.state = self.DEFAULT
        elif self.state == self.COLLISION:
            self.state = self.WAIT_RESET
        elif self.state == self.RESET:
            self.state = self.WAIT_FIRST_FLAP

        
