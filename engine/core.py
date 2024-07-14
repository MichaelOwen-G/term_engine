import curses
import os
import time
from typing import List

from .systems.FrameTimeKeeper import FrameTimeKeeper
from .systems.TypingSystem import TypingSystem
from .systems.RenderingSystem import RenderingSystem
from .systems.CollisionSystem import CollisionSystem

from .engine_interface import EngineInterface

from .components._interfaces import ColliderInterface, ObjectInterface

from .systems._interfaces import EngineSystem


class GameEngine(EngineInterface):
    def __init__(self, window_width: int, window_height: int):
        EngineInterface.__init__(self, window_width, window_height)
        
        # initialize curses
        self.initialize_curses()
        self._config_window(window_height, window_width)

        ''' FRAME TIME KEEPER'''
        self.frame_time_keeper: FrameTimeKeeper = FrameTimeKeeper()

        
        self.rendering_system: RenderingSystem = RenderingSystem(self)
        ''' To handle rendering the objects, we will need to run the rendering system on individual objects '''

        
        self.collision_system: CollisionSystem = CollisionSystem(self)
        ''' To handle collisions, we will need to run the collision system on individual objects '''


        self.typing_system: TypingSystem = TypingSystem(self)
        ''' To handle key presses, we will need to run the typing system on individual objects '''


        self.engine_systems: List[EngineSystem] = []
        ''' ENGINE SYSTEMS 
        - These are systems that will be run on/against the engine
        '''


        ''' ENGINE EFFECTS'''
        self.engine_effects: list = [
            # These are effects like SpawnEffect
        ]

        ''' OBJECTS '''
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

    def _config_window(self, height: int, width: int):
        ''' Configures the CLI window '''
        window_confid_command: str = f'mode con: cols={width} lines={height}'
        os.system(window_confid_command)

    def run(self):
        
        # create game loop
        while True:
            # print('OBJECTS')
            # print(self.objects)
            # time.sleep(1)
            print()
            print('FRAME ===========================================')
               
            # run delta time keeper
            self.frame_time_keeper.run()

            # get delta_time: milliseconds
            dt: float = self.frame_time_keeper.delta_time

            # ENGINE_SYSTEMS run independently
            # run engine systems
            for engine_sys in self.engine_systems:
                engine_sys.run(dt)

            # run EngineEffects from the engine
            for effect in self.engine_effects:
                effect.run(dt, self, None)

            # UPDATE GAME_ENGINE OBJECTS
            for object in self.objects:
                # print('OBJECT')
                # print(object)
                print('SIZE', object.size)
                print('POS', object.pos)
                # print('BOUNDS', object.bounds)
                # print('R FRONT BUFFER', object._front_buffer._buffer)
                # print('FRONT BUFFER', object.front_buffer)

                # handle key presses
                if (object.listen_to_keys): self.typing_system.run(dt, object)

                # run object effects
                for effect in object.effects:
                    if effect.shouldRun(dt):
                        effect.run(dt, self, object)

                # Update Engine Objects
                object.update(dt, self)

                 # handle collisions if object has a collider
                if isinstance(object, ColliderInterface):
                    self.collision_system.run(dt, object)
                
                # render the object
                self.rendering_system.run(dt, object)


class Game(GameEngine):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def addObject(self, obj: ObjectInterface):
        ''' Takes an object of type ObjectInterface and adds it to the game engine '''

        if not isinstance(obj, ObjectInterface):
            raise Exception('Object is not of type ObjectInterface')
        
        self.objects.append(obj)

        # if the object's tag is not '' and does not exist yet, add it to the engine's attrs
        if (obj.tag != '') and (not hasattr(self, obj.tag)):
            setattr(self, obj.tag, obj)

    def findObjects(self, tag: str) -> List[ObjectInterface]:
        ''' Finds an object by its tag '''
        found_objs: List[ObjectInterface] = []

        for obj in self.objects:
            if obj.tag == tag:
                found_objs.append(obj)

        return found_objs

    def addEffect(self, effect):
        self.engine_effects.append(effect)


