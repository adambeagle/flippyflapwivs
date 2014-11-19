"""
resmaps.py
Author: Adam Beagle

PURPORSE:
  Ui modules should use the IMAGES and SOUNDS dicts from this module to
  retrieve paths to resource files. Resource file paths can then be changed
  only in this file without breaking anything.
"""
from os.path import abspath, dirname, join, pardir

# Root paths
_resource_root = abspath(join(dirname(__file__), pardir, 'res', ))
_image_path = join(_resource_root, 'images')
_sound_path = join(_resource_root, 'sounds')

# Public constants
IMAGES = {
    'tileset' : join(_image_path, 'tileset.png'),
}

SOUNDS = {
    'collision' : join(_sound_path, 'sad.ogg'),
    'music'     : join(_sound_path, 'music.ogg'),
    'score'     : join(_sound_path, 'score.ogg'),
}
