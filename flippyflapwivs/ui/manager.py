"""
manager.py
Author: Adam Beagle

PURPOSE:
  An instance of the UIManager class should be the sole interface
  between the main module and the ui subpackage. Main should call the
  instance's update() and draw() methods once per frame.

CONTENTS:
  AudioPlayer
  UIManager
"""
from adamlib.game.pygame.audio import AudioPlayer as BaseAudioPlayer
import pygame

from flippyflapwivs import CONFIG
from .resmaps import SOUNDS
from .background import BlueSkyBackground
from .level import Level
from .player import Wivs
from .sprites import Score
from .tileset import TILESET
from .util import game_coords_to_ui

class AudioPlayer(BaseAudioPlayer):
    """
    Handles all audio tasks (instantiating, playing, stopping, etc.)

    Update() should be called once per frame.
    """
    def __init__(self):
        super().__init__(SOUNDS)
        self.set_volume('music', 0.5)
        self.set_volume('collision', 0.5)

        if not CONFIG.MUTE:
            self._start_music()

    def update(self, gamestate, *args):
        gs = gamestate
        
        unmute = 'unmute' in gamestate.kwargs
        if unmute and gs.state != gs.WAIT_RESET:
            gamestate.kwargs.pop('unmute')
            self._start_music()
        
        if gs.state == gs.RESET:
            self.wait_until_sound_end()
            self._start_music()
        elif gs.state == gs.COLLISION:
            self.stop_all()
            self.play('collision')
        elif gs.state == gs.SCORE:
            self.play('score')

    def _start_music(self):
        self.play('music', loops=-1)

class UIManager:
    """
    Interface from main to the ui modules. Main should call update(),
    then draw() once per frame.
    """
    def __init__(self, n_columns, scroll_speed):
        self._screen = pygame.display.set_mode(
            CONFIG.SCREEN_SIZE,
            pygame.FULLSCREEN if CONFIG.FULLSCREEN else 0
        )

        # Display must be initialized before tileset init
        TILESET.init()

        scroll_speed = game_coords_to_ui(abs(scroll_speed))[0]
        background = BlueSkyBackground()
        self.level = Level(n_columns, scroll_speed)
        self.player = Wivs()

        # Note order is update/draw order
        self.sfcs = [background, self.level, self.player, Score()]

        self.audioplayer = AudioPlayer()

    def draw(self):
        """Call once per frame to draw all ui elements"""
        for sfc in self.sfcs:
            sfc.draw(self._screen)

        pygame.display.flip()

    def postupdate(self, gamestate, gamedata, dt):
        """
        Reserved for cases in which a state is set by a ui object which
        needs to be seen by another ui object updated prior to the
        state-setting object.
        """
        # Change player image on COLLISION
        if gamestate.state == gamestate.COLLISION:
            self.player.update(gamestate, gamedata, dt)

    def update(self, gamestate, gamedata, dt):
        """Call once per frame to update all ui elements."""
        for sfc in self.sfcs:
            sfc.update(gamestate, gamedata, dt)

        # Detect collision between player and level sprites
        if (gamestate.state != gamestate.WAIT_RESET and
            pygame.sprite.spritecollide(self.player, self.level.sprites,
                collided=pygame.sprite.collide_mask, dokill=False
        )):
            gamestate.state = gamestate.COLLISION

        # Update audio
        if not CONFIG.MUTE:
            self.audioplayer.update(gamestate)
            
        elif 'mute' in gamestate.kwargs:
            self.audioplayer.stop_all()
            gamestate.kwargs.pop('mute')
            
        elif gamestate.state == gamestate.RESET:
            # Small delay to make up for wait_until_sound_end when unmuted
            pygame.time.wait(1000)

        self.postupdate(gamestate, gamedata, dt)


