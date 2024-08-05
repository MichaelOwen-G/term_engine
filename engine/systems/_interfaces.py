from abc import ABC, abstractmethod

from .._interface import EngineInterface

from ..components._interfaces import ObjectInterface

class EngineSystem(ABC):
    @abstractmethod
    def run(self, game_engine: EngineInterface):...

class ObjectSystem(ABC):
    @abstractmethod
    def run(self, object: ObjectInterface, game_engine: EngineInterface):...