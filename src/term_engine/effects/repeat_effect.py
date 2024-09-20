from enum import Enum
import inspect

from term_engine.effects._interfaces import Effect
from term_engine._interface import EngineInterface
from term_engine.components._interfaces import ObjectInterface

from term_engine.metrics.duration import Duration


class RepeatType(Enum):
    '''
    Defines the type of repeat that a RepeatEffect should use
    '''

    # Run the effect once in a duration provided
    ONCE_IN_DURATION = 1

    #Repeat the effect after every duration provided
    INDEFINETLY_EVERY_DURATION = 2

    # Run the effect once in next frame
    ONCE_IN_NEXT_FRAME = 3

    # Repeat the effect in every frame
    INDEFINETLY_EVERY_FRAME = 4
    
class RepeatEffect(Effect):
    def __init__(self, repeatType, duration):
        # the RepeatType of the effect
        # vaildate 
        if not isinstance(repeatType, RepeatType):
            raise TypeError(f'repeatType arg should be of type RepeatType, {type(duration)} given')
        
        self.repeatType: RepeatType = repeatType

        # the duration it should wait before callback
        # validate
        if not isinstance(duration, Duration):
            raise TypeError(f'duration should of type Duration, {type(duration)} given')
        
        self.duration: Duration = duration

        # stores the last time the effect was
        # ran to keep track of repeat times
        # in millisecs
        self._last_time_ran: float  = 0

        # stores the time past since the last time the effect was ran
        # in milliseconds
        self._time_past: float = 0

        self.running: bool = False
        
        super().__init__()

    def run(self, dt:float, game: EngineInterface, object: 'ObjectInterface|None'):
        # validate the arguments
        if not isinstance(dt, float):
            raise TypeError("dt must be of type float is type " + str(type(dt)))
        
        if not isinstance(object, ObjectInterface):
            if  object is not None:
                raise TypeError("object must be of type Object or None")
    
    def dispose(self):...
    
    def shouldRun(self, dt:float) -> bool:
        '''
        Checks if the effect should run based on the repeatType and last_time_ran
        - Gets dt in milliseconds
        '''

        shouldRun: bool = False

        # print(dt, 'ms since last ran')
        # print(self._time_past, 'ms time_past')
        # print(self._last_time_ran, 'ms last_time_ran')
        # print(self.duration.milliSeconds, 'ms duration')

        match self.repeatType:
            case RepeatType.ONCE_IN_NEXT_FRAME:
                # runs for the first frame only when last_time_ran is 0
                shouldRun = True if self._last_time_ran == 0 else False
            case RepeatType.ONCE_IN_DURATION:
                # if the time_past is greater or equal to the duration of repeat
                # run, if the effect has not run before
                if (self._time_past >= self.duration.milliSeconds and self._last_time_ran == 0): 
                    shouldRun = True
            case RepeatType.INDEFINETLY_EVERY_FRAME:
                # always true cos it runs every frame
                shouldRun = True
            case RepeatType.INDEFINETLY_EVERY_DURATION:
                # if the time_past is greater or equal to the duration of repeat
                # the effect should run
                if (self._time_past >= self.duration.milliSeconds and self._time_past != 0): 
                    shouldRun = True
            
        # assign self._last_time_ran with the current time if the effect should run
        if shouldRun: self._last_time_ran += dt

        # increment self._time_past with delta time if the effect should not run
        # clear self._time_past if the effect should run
        self._time_past += dt if not shouldRun else  - self._time_past

        # print('shouldRun', shouldRun)

        # return should_run
        return shouldRun


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
        - The callback is provided with the following kwrags
          - dt: The time since the last frame
          - game: The game object
          - object: The object that the effect is applied to

        '''

        # validate the callback argumet
        # self._validate_callback(callback)

        # add to list of callbacks
        self._callbacks.append(callback)

    def removeCallback(self, callback:callable):
        ''' Removes the callback from the effect'''
        self._callbacks.remove(callback)

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

    
    def run(self, dt: float, game, object: ObjectInterface):
        super().run(dt, game, object)

        # run all the callbacks
        for callback in self._callbacks:
            callback(dt = dt, game = game, effect = self, object = object)
