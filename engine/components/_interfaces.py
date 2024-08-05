from abc import ABC, abstractmethod
from typing import List

from ..utils.pars_type_sensitivity import ParsTypeSensitivity

from ..metrics.vec2 import Vec2

class ObjectInterface(ParsTypeSensitivity):
    def __init__(self, drawing, tags, isPersistent):
        ParsTypeSensitivity.__init__(self,
                                     self.__class__.__name__,
                                     [
                                         ('drawing', drawing, DrawingInterface),
                                         ('tag', tags, list),
                                         ('isPersistent', isPersistent, bool)
                                     ])
         
        self.drawing: DrawingInterface = drawing
        self.tags: list[str] = tags

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

        self.isGarbage = False # if true, the object will not be disposed
        self.isPersistent = isPersistent # if true, the object will not be disposed when out of view

    @abstractmethod
    def onMount(self, game = None, screen = None):...

    @abstractmethod
    def update(self, dt: float, game):...
    
    @abstractmethod
    def render(self):...
    
    @abstractmethod
    def dispose(self):...


class ColliderInterface(ParsTypeSensitivity):
    def __init__(self, colliderFill) -> None:
        ParsTypeSensitivity.__init__(self, 
                                     self.__class__.__name__, 
                                     [])
        
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


class DrawingInterface(ParsTypeSensitivity):
    def __init__(self, tag: str, maxWidth: int, maxHeight: int) -> None:
        ParsTypeSensitivity.__init__(self, 
                                     self.__class__.__name__,
                                     [
                                         ('tag', tag, str),
                                         ('maxWidth', maxWidth, int),
                                         ('maxHeight', maxHeight, int),
                                     ])
        
        self.tag = tag

        # to track the constraints of the drawing
        self.maxWidth: int = maxWidth
        self.maxHeight: int = maxHeight

    @property
    def maxSize(self) -> Vec2:
        return Vec2(self.maxWidth, self.maxHeight)

    def draw(self, stringDrawing, stripNewLines, fillBlanks): pass



class DrawingStackInterface(ParsTypeSensitivity):
    def __init__(self):
        ParsTypeSensitivity.__init__(self,
                                     self.__class__.__name__,
                                     [])
        
        self.drawings: List[DrawingInterface] = []

    @abstractmethod
    def add(drawing, stackDirection, alignment) -> None: 
        pass