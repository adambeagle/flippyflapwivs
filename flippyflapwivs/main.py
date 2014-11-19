"""
main.py
Author: Adam Beagle

PURPOSE:
  Game entry point and main loop.

USAGE:
  Run this file with a Python interpreter to run the game.
  Run with the -h option to view optional argument details (also available
  in README.rst).
"""
from argparse import ArgumentParser
from os import environ, path
from sys import path as syspath

import pygame

# Add root directory to sys.path if package not installed
try:
    from flippyflapwivs import CONFIG
except ImportError:
    syspath.append(
        path.abspath(path.join(path.dirname(__file__), path.pardir))
    )
    from flippyflapwivs import CONFIG
    
from game import GameData, GameState
from ui import UIManager

def main():
    parse_args() # Sets CONFIG options.
                 # Must be called before UIManager instantiated.
    
    pygame.init()
    pygame.display.set_caption('Flippyflap Wivs')
    environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    
    clock = pygame.time.Clock()
    dt = 1
    gdt = 60 / CONFIG.FPS_LIMIT
    gs = GameState()
    gd = GameData()
    uim = UIManager(gd.n_columns, gdt*gd.scroll_speed)

    pygame.mouse.set_visible(0)
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(
        (pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEBUTTONDOWN)
    )

    # Game loop
    while True:
        # Transition state
        gs.transition_state()
        
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                handle_event_keydown(gs, event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_event_mousebuttondown(gs, event)

        if gs.state == gs.QUIT:
            return

        if gs.state != gs.PAUSE:
            # Update
            gd.update(gs, gdt)
            uim.update(gs, gd, dt)
            gd.postupdate(gs, gdt)

            # Draw
            uim.draw()

        # Cleanup
        clock.tick(CONFIG.FPS_LIMIT)
        fps = clock.get_fps()
        gdt = 60 / (fps if fps > 15 else CONFIG.FPS_LIMIT)                                       
        dt = fps / CONFIG.FPS_LIMIT
        pygame.event.pump()

    pygame.quit()

def handle_event_keydown(gamestate, event):
    gs = gamestate
    if event.key == pygame.K_q:
        gs.state = gs.QUIT
        
    elif event.key == pygame.K_p:
        if gs.state == gs.PAUSE:
            gs.state = gs.previous
        else:
            gs.state = gs.PAUSE
            
    elif event.key == pygame.K_m:
        if CONFIG.MUTE:
            CONFIG.MUTE = False
            gamestate.kwargs['unmute'] = True
        else:
            CONFIG.MUTE = True
            gamestate.kwargs['mute'] = True
        
    elif (gs.state in (gs.WAIT_FIRST_FLAP, gs.DEFAULT) and
        event.key == pygame.K_SPACE
    ):
        gs.state = gs.FLAP

def handle_event_mousebuttondown(gamestate, event):
    gs = gamestate
    if gs.state in (gs.WAIT_FIRST_FLAP, gs.DEFAULT) and event.button == 1:
        gs.state = gs.FLAP

def parse_args():
    """Parse command line args and instantiate CONFIG constants."""
    parser = ArgumentParser(description='Play FlippyFlap Wivs.')
    parser.add_argument('-f', '--fullscreen', action='store_true')
    parser.add_argument('-r', '--resolution', nargs=2, type=int,
        default=(800, 600), help='Screen resolution in px: width height',
        metavar=('W', 'H')
    )
    parser.add_argument('--fps', type=int, default=120, choices=range(30, 121),
        metavar='int', help='int in [30, 121)'
    )
    parser.add_argument('-m', '--mute', action='store_true',
        help="Disable sounds."
    )
    args = parser.parse_args()
    
    CONFIG.FPS_LIMIT = args.fps
    CONFIG.FULLSCREEN = args.fullscreen
    CONFIG.MUTE = args.mute
    CONFIG.SCREEN_SIZE = args.resolution

    # Lock CONFIG so options (except for mute) can no longer be set
    CONFIG.lock()

###############################################################################
if __name__ == '__main__':
    main()
