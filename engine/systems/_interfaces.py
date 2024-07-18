from abc import ABC, abstractmethod

from .._interface import EngineInterface

from ..components._interfaces import ObjectInterface

class EngineSystem(ABC):
    def __init__(self, game_engine):
        self.game_engine: EngineInterface = game_engine

    @abstractmethod
    def run(self):
        pass

class ObjectSystem(ABC):
    def __init__(self, game_engine: EngineInterface):
        self.game_engine: EngineInterface = game_engine

    @abstractmethod
    def run(self, object: ObjectInterface):
        pass