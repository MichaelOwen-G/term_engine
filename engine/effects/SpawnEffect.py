import inspect

from ..components._interfaces import ObjectInterface
from ..engine_interface import EngineInterface

from .RepeatEffect import RepeatEffect, RepeatType

from ..metrics.duration import Duration


class SpawnEffect(RepeatEffect):
    '''
        Defines a RepeatEffect that spawns an object on RepeatEffect run
    '''

    def __init__(self, repeatType: RepeatType, duration: Duration, object_factory: callable):
        '''
        # Spawn Effect
        Requires a repeatType: RepeatType, duration: Duration and an object_factory: callable
        The object_factory is a callable that will be called when the effect is ran
         - The callable should take in 2 arguments:
            - a gameInstance: (game: Game)
            - delta time: (dt: int)
         - The callable should return an object: Object that will be added to the gameInstance.objects list
         # Example of object_factory callable
        ```
        def object_factory(game: Game, dt: int) -> Object:
            return Object()
                
        pipe_spawner = SpawnEffect(RepeatType.ONCE_IN_DURATION, Duration(1000), object_factory)
        ```
        '''

        # validate the object_factory argument
        self._validate_object_factory(object_factory)

        self._object_factory = object_factory
        super().__init__(repeatType, duration)

    def _validate_object_factory(self, object_factory: callable):
        '''
        Validates the object_factory
        - Checks if the object_factory takes in 2 arguments
        - throws an error if it takes less or more
        - Checks if the object_factory returns an Object
        - throws an error if it returns anything else
        '''

        ''' VALIDATE PARAMETERS'''
        # get information about the function
        signature = inspect.signature(object_factory)

        # get the parameters of the function
        pars = signature.parameters

        # validate the length of the parameters
        if (len(pars)!= 2):
            raise ValueError("Object Factories should take in exactly 2 arguments. Object Factory", object_factory, " requires ", len(pars), "arguments")
        
        ''' VALIDATE RETURN TYPE'''
        # get the return type of the function
        return_type = signature.return_annotation

        # validate the return type
        if isinstance(return_type, ObjectInterface):
            raise ValueError("Object Factories should return an Object. Object Factory", object_factory, " returns ", return_type)

    def run(self, dt: int, game_engine: EngineInterface, object: None):
        super().run(dt, game_engine, object)

        # spawn the object
        spawnedObj = self._object_factory(game_engine, dt)

        # add the object to the game
        game_engine.objects.append(spawnedObj)

