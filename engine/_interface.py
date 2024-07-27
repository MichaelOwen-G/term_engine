from abc import ABC, abstractmethod
from typing import List

from engine.components._interfaces import ObjectInterface


class EngineInterface(ABC):
    '''
    Defines the interface for the game engine
    '''
    def __init__(self, window_width: int, window_height: int, debug_mode: bool, frame_cap: int):
        ''' MUST HAVE THE FOLLOWING FIELDS'''
        self.frame_time_keeper = None

        self.rendering_system = None
        
        self.collision_system = None

        self.typing_system = None

        self.engine_systems = None
        
        self.engine_effects: list = []

        self.objects: list = []

        self.debug_mode: bool = debug_mode

        self.frame_cap = frame_cap

        self.running = True

        '''METRICS'''
        self.window_width = window_width
        self.window_height = window_height

        self.floor = self.window_height - 2
        self.roof = 1

        # UTILIZES curses
        self.stdscr = None

    ''' MUST HAVE THE FOLLOWING METHODS'''
    @abstractmethod
    def run(self):...

    def update(self, dt: int):...


class GameScreenInterface(ABC):
    def __init__(self):

        ''' ENGINE EFFECTS'''
        self.screen_effects: list = [
            # These are effects like SpawnEffect
        ]

        ''' OBJECTS ARRAY '''
        self.objects: list[ObjectInterface] = []

    def addObject(self, obj: ObjectInterface):
        # set the object's game instance
        obj.game = self
        # add the object to the game
        self.objects.append(obj)
        # call object onMount method
        obj.onMount()

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
    def update(self, dt:int):...

    @abstractmethod
    def onLaunch(self):...

    @abstractmethod
    def onCreate(self):...