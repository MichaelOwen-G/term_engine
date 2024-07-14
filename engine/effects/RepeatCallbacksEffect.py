
import inspect

from .RepeatEffect import RepeatEffect, RepeatType

from ..components._interfaces import ObjectInterface

from ..metrics.duration import Duration

class RepeatCallbacksEffect(RepeatEffect):
    '''
    - Defines a RepeatEffect class that can be applied to an object
    - It executes a list of callbacks on RepeatEffect.run
    '''
    def __init__(self, repeatType: RepeatType, duration: Duration = None):
        self._callbacks: list[callable] = []
        super().__init__(repeatType, duration)

    def addCallback(self, callback: callable):
        '''
        Adds a callback to the effect:
        - The callback should be a function that takes in 3 arguments
          - dt: The time since the last frame
          - game: The game object
          - object: The object that the effect is applied to

        '''

        # validate the callback argumet
        self._validate_callback(callback)

        # add to list of callbacks
        self._callbacks.append(callback)

    def _validate_callback(self, callback: callable):
        '''
        Validates the callback
        - Checks if the callback takes in 3 arguments
            - dt: The time since the last frame
            - game: The game instance
            - object: The object that the effect is applied to
        - throws an error if it takes less or more
        '''

        # get information about the function
        signature = inspect.signature(callback)

        # get the parameters of the function
        params = signature.parameters

        if len(params) != 3:
            raise ValueError("Effect Callbacks should take in exactly 3 arguments. Callback", callback, " requires ", len(params), "arguments")

    
    def run(self, dt: float, game_engine, object: ObjectInterface):
        super().run(dt, game_engine, object)

        # run all the callbacks
        for callback in self._callbacks:
            callback(dt, game_engine, object)


