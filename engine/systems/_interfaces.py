from abc import ABC, abstractmethod

from ..engine_interface import EngineInterface

from ..components._interfaces import ObjectInterface

class EngineSystem(ABC):
    def __init__(self, game_engine):
        self.game_engine: EngineInterface = game_engine

    @abstractmethod
    def run(self, dt: float):
        pass

class ObjectSystem(ABC):
    def __init__(self, game_engine: EngineInterface):
        self.game_engine: EngineInterface = game_engine

    @abstractmethod
    def run(self, dt: float, object: ObjectInterface):
        pass