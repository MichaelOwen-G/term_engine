from abc import ABC
import curses
import os
import time
from typing import List, override

from .systems.garbage_collection_system import GarbageCollectionSystem
from .systems.frame_time_keeper import FrameTimeKeeper
from .systems.rendering_system import RenderingSystem
from .systems.collision_system import CollisionSystem

from ._interface import EngineInterface, GameScreenInterface

from .components._interfaces import ColliderInterface, ObjectInterface


class GameEngine(EngineInterface):
    def __init__(self, window_width: int, window_height: int, debug_mode: bool, frame_cap: int ):
        EngineInterface.__init__(self, window_width, window_height, debug_mode, frame_cap)
        
        # initialize curses
        if not debug_mode:
            self.initialize_curses()
            self._config_window(window_height, window_width)

        self.debug_mode = debug_mode
        
        
        ''' ENGINE SYSTEMS'''
        self.frame_time_keeper: FrameTimeKeeper = FrameTimeKeeper(self)
        ''' FRAME TIME KEEPER'''

        self.garbage_collector = GarbageCollectionSystem(self)
        ''' To Handle the disposal of garbaged objects, we will need to run the garbage collector '''


        ''' OBJECT SYSTEMS'''
        self.rendering_system: RenderingSystem = RenderingSystem(self)
        ''' To handle rendering the objects, we will need to run the rendering system on individual objects '''

        self.collision_system: CollisionSystem = CollisionSystem(self)
        ''' To handle collisions, we will need to run the collision system on individual objects '''

        
        self.game_screen: GameScreenInterface = None
        ''' The game screen feeding the engine'''

    @property
    def collidable_objects(self):
        ''' returns all objects that have a collider '''
        return [obj for obj in self.game_screen.objects if isinstance(obj, ColliderInterface)]
    
    @collidable_objects.setter
    def collidable_objects(self, _): pass

    def initialize_curses(self):
        # initialize curses
        self.stdscr = curses.initscr()

        curses.curs_set(0)  # Hide cursor
        curses.noecho()  # Don't echo keystrokes

        self.stdscr.nodelay(True) # avoid waiting for key presses


    def _config_window(self, height: int, width: int):
        ''' Configures the CLI window '''
        window_confid_command: str = f'mode con: cols={width} lines={height}'
        os.system(window_confid_command)

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def update(self, dt: int):...

    def run(self):
        
        # create game loop
        while True:
            
            if self.debug_mode: 
                time.sleep(1)
                print()
                print('================= FRAME ===========================')
                print(f'FPS: {self.frame_time_keeper.fps} | DT: {self.frame_time_keeper.delta_time}ms')
                print(f'OBJECTS: {len(self.game_screen.objects)}')

            # run delta time keeper
            self.frame_time_keeper.run()

            # run garbage collector
            self.garbage_collector.run()

            # get delta_time: milliseconds
            dt: float = self.frame_time_keeper.delta_time
            
            # run EngineEffects of the game_screen meant from the engine
            for effect in self.game_screen.screen_effects:
                if effect.shouldRun(dt): effect.run(dt, self, None)

            # UPDATE GAME_ENGINE OBJECTS
            for object in self.game_screen.objects:

                # run object effects
                for effect in object.effects:
                    if effect.shouldRun(dt): effect.run(dt, self, object)

                # Update Engine Objects
                object.update(dt, self)

                 # handle collisions if object has a collider
                if isinstance(object, ColliderInterface): self.collision_system.run(object)

                self.rendering_system.run(object) 

            # CALL GAME UPDATE FUNCTION
            self.update(dt)      

            if not self.running: break     


class Game(GameEngine, GameScreenInterface):
    def __init__(self, width: int = 50, height: int = 50, debug_mode: bool = False, frame_cap:int = 900):
        super().__init__(width, height, debug_mode=debug_mode, frame_cap=frame_cap)
        GameScreenInterface.__init__(self)

        self.game_screens: list[GameScreen] = []

        self.current_screen_ind: int = -1

        self.screens_stack: list[int] = []

        # call on create
        self.onCreate()

    def onLaunch(self):
        print(f'screens 0nLaunxch {self.game_screens}')

    def run(self):
        self.onLaunch()

        return super().run()

    def onCreate(self):
        print(f'screens 0ncreate {self.game_screens}')
        # if this has game_screens len > 0
        if len(self.game_screens) == 0: self.game_screen = self

        print(f'screens 0ncreate2 {self.game_screens}')
        # switch to the first screen
        self.switchToScreenByTag(self.game_screens[0].tag)

    @override
    def update(self, dt: int):
        if self.game_screen is not self:
            self.game_screen.update(dt)

        return super().update(dt)

    def find_screen_by_tag(self, tag:str):
        if isinstance(self, GameScreen): return [scr for scr in self.game.game_screens if tag in scr.tags]

        return [scr for scr in self.game_screens if tag == scr.tag]
    
    def addScreen(self, screen: 'GameScreen'):
        
        self.game_screens.append(screen)
        screen.onCreate()

    def switchToScreenByTag(self, tag:str):
        print(f'switching to {self.game_screens}')
        # find next screen with tag
        scrs = self.find_screen_by_tag(tag)

        # close if screen doesn't exist
        if len(scrs) == 0: return

        # get it if it does
        next_screen: GameScreen = scrs[0]

        # clear engine screen
        if not self.debug_mode: self.clear_screen()

        # switch the engine's game_screen to next_screen
        self.game_screen = next_screen

        # set current screen
        self.current_screen_ind = self.game_screens.index(next_screen)

        # call onLaunch for next screen
        next_screen.onLaunch()

        # add toscreen stack
        self.screens_stack.append(self.current_screen_ind)

    def switchToBack(self):
        # back out if scree stack is non-existent
        if len(self.screens_stack) < 1: return

        # get previous screen from the last screen in screen_stack
        prev_scr_ind = len(self.screens_stack) - 2
        prev_screen = self.game_screens[prev_scr_ind]

        # update screen stack
        # scr before prev_screen should be the last screen in the stack
        self.screens_stack = self.screens_stack[:prev_scr_ind]

        # switch to previous screen
        self.switchToScreen(prev_screen.tag)

class GameScreen(GameScreenInterface):
    def __init__(self, tag):
        GameScreenInterface.__init__(self)
        self.tag = tag

    @override
    def onLaunch(self):
        return super().onLaunch()

    @override
    def update(self, dt:int):
        return super().update(dt)
    
    def onCreate(self):
        return super().onCreate()
