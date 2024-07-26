import curses
import os
import time
from typing import List

from .systems.garbage_collection_system import GarbageCollectionSystem
from .systems.frame_time_keeper import FrameTimeKeeper
from .systems.rendering_system import RenderingSystem
from .systems.collision_system import CollisionSystem

from ._interface import EngineInterface

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

        
        
        ''' ENGINE EFFECTS'''
        self.engine_effects: list = [
            # These are effects like SpawnEffect
        ]

        ''' OBJECTS ARRAY '''
        self.objects: list[ObjectInterface] = []

    @property
    def collidable_objects(self):
        ''' returns all objects that have a collider '''
        return [obj for obj in self.objects if isinstance(obj, ColliderInterface)]
    
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

    def update(self, dt: int):
        pass

    def run(self):
        
        # create game loop
        while True:
            
            if self.debug_mode: 
                time.sleep(1)
                print()
                print('================= FRAME ===========================')
                print(f'FPS: {self.frame_time_keeper.fps} | DT: {self.frame_time_keeper.delta_time}ms')

                print('OBJECTS')
                print(len(self.objects))
               
            # run delta time keeper
            self.frame_time_keeper.run()

            # run garbage collector
            self.garbage_collector.run()

            # get delta_time: milliseconds
            dt: float = self.frame_time_keeper.delta_time

            
            # run EngineEffects from the engine
            for effect in self.engine_effects:
                if effect.shouldRun(dt): effect.run(dt, self, None)

            # UPDATE GAME_ENGINE OBJECTS
            for object in self.objects:

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


class Game(GameEngine):
    def __init__(self, width: int = 50, height: int = 50, debug_mode: bool = False, frame_cap:int = 900):
        super().__init__(width, height, debug_mode=debug_mode, frame_cap=frame_cap)

        # call on launch
        self.onLaunch()

    def onLaunch(self):...
    def update(self, dt: int):...


    def addObject(self, obj: ObjectInterface):
        ''' Takes an object of type ObjectInterface and adds it to the game engine '''

        if not isinstance(obj, ObjectInterface):
            raise Exception('Object is not of type ObjectInterface')
        
        # set the object's game instance
        obj.game = self

        # add the object to the game
        self.objects.append(obj)

        # call object onMount method
        obj.onMount()

    def addObjects(self, objs: List[ObjectInterface]):
        [self.addObject(obj) for obj in objs]

    def find_objects_by_tag(self, tag: str) -> List[ObjectInterface]:
        ''' Finds an object by its tag '''
        found_objs: List[ObjectInterface] = []

        for obj in self.objects:
            if tag in obj.tags: found_objs.append(obj)

        return found_objs

    def addEffect(self, effect):
        self.engine_effects.append(effect)

    


