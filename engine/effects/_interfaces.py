from abc import ABC, abstractmethod

from ..components._interfaces import ObjectInterface
from ..engine_interface import EngineInterface


class Effect(ABC):
    @abstractmethod
    def run(self, dt:int, game_engine: EngineInterface, object: ObjectInterface):
        pass

    @abstractmethod
    def shouldRun(self, dt: float):
        pass

'''
class EngineEffect(ABC):
    def __init__(self, game_engine: Game):
        self.game_engine = game_engine

    @abstractmethod
    def run(self, dt:float):
        pass
    
    def shouldRun(self, dt: float):
        pass
'''