from abc import ABC, abstractmethod

from term_engine.components._interfaces import ObjectInterface

class EngineSystem(ABC):
    @abstractmethod
    def run(self, game_engine):...

class ObjectSystem(ABC):
    @abstractmethod
    def run(self, object: ObjectInterface, game_engine):...