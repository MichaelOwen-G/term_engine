from abc import ABC, abstractmethod
from typing import List

from engine.metrics.vec2 import Vec2

class ObjectInterface(ABC):
    def __init__(self, drawing: 'DrawingInterface', tag: str = ""):
        
        # validate the inputted drawing object
        if not isinstance(drawing, DrawingInterface):
            raise TypeError(f"Drawing must be of type Drawing or DrawingStack. Instead, Type {type(drawing)} was provided")
        else:
            self.drawing: DrawingInterface = drawing

        # validate tag type
        if not isinstance(tag, str):
            raise TypeError("tag must be of type str")
        else:
            self.tag: str = tag

        self.effects: list = []
        self.listen_to_keys = False

        ''' POSITION FLAGS'''
        self.in_view = True

        self.on_floor = False
        self.below_floor = False

        self.on_roof = False
        self.above_roof = False

        self.past_right_extreme = False
        self.past_left_extreme = False

    @abstractmethod
    def update(self, dt: float):
        pass
    
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def shouldRerender(self) -> bool:
        pass


class ColliderInterface(ABC):
    def __init__(self, colliderFill) -> None:
        self.colliderFill = colliderFill
        self._collisions = []

    @property
    def collisions(self):
        return self._collisions
    
    @collisions.setter
    def collisions(self, _): pass

    def clear_collisions(self): self._collisions = []

    @abstractmethod
    def collide_with(self, other: 'ColliderInterface'): pass


class DrawingInterface(ABC):
    def __init__(self, tag: str) -> None:
        self.tag = tag

        # to track the constraints of the drawing
        self.maxWidth: int = 0
        self.maxHeight: int = 0

    @property
    def maxSize(self) -> Vec2:
        return Vec2(self.maxWidth, self.maxHeight)

    def draw(self, stringDrawing, stripNewLines, fillBlanks): pass

class DrawingStackInterface(ABC):
    def __init__(self):
        self.drawings: List[DrawingInterface] = []

    @abstractmethod
    def add(drawing, stackDirection, alignment) -> None: pass