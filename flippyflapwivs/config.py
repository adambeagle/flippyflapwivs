"""
config.py
Author: Adam Beagle

PURPOSE:
  Contains Config, a wrapper object for configuration "constants" which permits
  an initial set (from e.g. command line options) and provides a lock()
  method to prevent further changes.

Yes, there are global state problems here, it would take no real effort
to get around the _locked attribute, and if some module imported Config rather
than the global constant, depending on when it was imported, _locked could have
multiple reported states within the program. I don't claim this to be a great
design pattern, just minimal protection on a silly one-man project.
"""
class ConfigLockError(Exception):
    pass

class Config:
    """
    Configuration wrapper.

    ATTRIBUTES:
      FPS_LIMIT (read-only once locked)
      FULLSCREEN (read-only once locked)
      MUTE (r/w)
      SCREEN_SIZE (read-only once locked)

    METHODS:
      lock

    USAGE:
      It is expected that a global instance of CONFIG be created at some early
      point by main or the top-level __init__, and that lock() is called
      once the config options are instantiated.
    """
    MUTE = None
    _fps_limit = None
    _fullscreen = None
    _screenres = None
    _locked = False

    @classmethod
    def lock(cls):
        cls._locked = True

    @property
    def FPS_LIMIT(self):
        return self._fps_limit

    @FPS_LIMIT.setter
    def FPS_LIMIT(self, val):
        if self._locked:
            raise ConfigLockError(
                "Cannot set FPS_LIMIT once Config is locked."
            )

        self._fps_limit = val

    @property
    def FULLSCREEN(self):
        return self._fullscreen

    @FULLSCREEN.setter
    def FULLSCREEN(self, val):
        if self._locked:
            raise ConfigLockError(
                "Cannot set FULLSCREEN once Config is locked."
            )

        self._fullscreen = val

    @property
    def SCREEN_SIZE(self):
        return self._screenres

    @SCREEN_SIZE.setter
    def SCREEN_SIZE(self, val):
        if self._locked:
            raise ConfigLockError(
                "Cannot set SCREEN_SIZE once Config is locked."
            )

        self._screenres = val
