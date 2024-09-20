from abc import ABC, abstractmethod
import curses
import os
from typing import List

import pygame

from term_engine.components._interfaces import ObjectInterface

class EngineInterface(ABC):
    '''
    Defines the interface for the game engine
    '''
    def __init__(self, window_width: int, window_height: int, debug_mode: bool, frame_cap: int):
        ''' MUST HAVE THE FOLLOWING FIELDS'''
        self.frame_time_keeper = None

        self.rendering_system = None
        
        self.collision_system = None

        self.debug_mode: bool = debug_mode

        self.frame_cap = frame_cap

        self.running = True

        '''METRICS'''
        self.window_width = window_width
        self.window_height = window_height 

        self.floor = self.window_height - 6
        self.roof = 1

        # UTILIZES curses
        self.stdscr = None
        
    def init(self):
        self.init_curses() # start screen
        self._config_window() # resize cli window
        self.init_pygame() # initilaize sound
    
    def dispose(self):
        pygame.mixer.quit()
    
    
    ''' CURSES FUNCTIONS '''
    def init_curses(self):
        # initialize curses
        self.stdscr = curses.initscr()
        self.stdscr.box()

        curses.curs_set(0)  # Hide cursor
        curses.noecho()  # Don't echo keystrokes

        self.stdscr.nodelay(True) # avoid waiting for key presses
    
    def _config_window(self): # resize the cli window
        ''' Configures the CLI window '''
        window_confid_command: str = f'mode con: cols={self.window_width} lines={self.window_height}'
        os.system(window_confid_command)

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()


    ''' SOUND ASSETS FUNCTIONALITY '''
    # initialize pygame mixer
    def init_pygame(self): pygame.mixer.init()
    def exit_pygame(self): pygame.mixer.quit()
        
    # Loading sound
    def load_sound(self, file_path:str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(file_path) if not self.debug_mode else _SoundShell()
        
    ''' MUST HAVE THE FOLLOWING METHODS'''       
    @abstractmethod
    def run(self):...

    def update(self, dt: int, game):...
    
class _SoundShell:
    def play(self):...
    def stop(self):...


class GameScreenInterface(ABC):
    def __init__(self):

        ''' ENGINE EFFECTS'''
        self.screen_effects: list = []
        '''These are effects like SpawnEffect'''

        ''' OBJECTS ARRAY '''
        self.objects: list[ObjectInterface] = []

        self.game_instance = None
        ''' Is None if this is Game and not None if this is of type GameScreen '''

    def addObject(self, obj: ObjectInterface):
        self.objects.append(obj) # add the object to the game
        
        obj.onMount(
            game = self.game_instance if self.game_instance is not None else self,
            screen = self,
            ) # call object onMount method

    def removeObject(self, object):
        self.objects.remove(object)

        return self.objects

    def removeObjectsAny(self, tags: list[str]) -> list[ObjectInterface]:
        for obj in self.objects:
            for tag in tags:
                if tag in obj.tags:
                    self.objects.remove(obj)
                    break

        return self.objects

    def removeObjectsAll(self, tags: list[str]) -> list[ObjectInterface]:
        for obj in self.objects:
            for tag in tags:
                if tag not in obj.tags: break

                if obj == self.objects[-1]: 
                    self.objects.remove(obj)

        return self.objects

    def addObjects(self, objs: List[ObjectInterface]): 
        [self.addObject(obj) for obj in objs]

    def addEffect(self, effect): 
        self.screen_effects.append(effect)

    def find_objects_by_tag(self, tag: str) -> List[ObjectInterface]:
        ''' Finds an object by its tag '''
        return [obj for obj in self.objects if tag in obj.tags]

    @abstractmethod
    def update(self, dt:int, game):...

    @abstractmethod
    def onLaunch(self):...

    @abstractmethod
    def onCreate(self):...
