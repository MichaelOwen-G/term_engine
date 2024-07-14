
from ..components._interfaces import ObjectInterface
from ..systems._interfaces import ObjectSystem

class RepeatEffectSystem(ObjectSystem):
    ''' Responsible for handling all the RepeatEffect '''

    def __init__(self, game_engine):
        super().__init__(game_engine)

    def run(self, dt: float, object: ObjectInterface):
        '''' Handles the calling or updating all the RepeatEffects provided by an object '''
   
        # run all the objects effects that want to run in this frame
        for effect in object.effects:
            if (effect.shouldRun(dt)):
                effect.run(dt, self.game_engine, object)

