from .vec2 import Vec2

class Bounds:
    ''' Holds the bounds of an object '''
    def __init__(self, size: Vec2, pos: Vec2):
        self._size = size
        self._pos = pos
        
        self._define_bounds() # define bounds

    ''' SETTERS AND GETTERS FOR PROPERTIES '''
    @property
    def size(self) -> Vec2:
        ''' Returns the size of the bounds '''
        return self._size
    
    @size.setter
    def size(self, new_size: Vec2):
        ''' Sets the size of the bounds '''
        self._size = new_size
        self._define_bounds() # redefine bounds

    @property
    def pos(self) -> Vec2:
        ''' Returns the position of the bounds '''
        return self._pos
    
    @pos.setter
    def pos(self, new_pos: Vec2):
        ''' Sets the position of the bounds '''
        self._pos = new_pos
        self._define_bounds() # redefine bounds 

    def _define_bounds(self):
        # where the object's width extent starts on the screen
        self.x_start = self._pos.x
         # where the object's width extent ends on the screen
        self.x_end = self._pos.x + self._size.x
        # where the object's height extent starts on the screen
        self.y_start = self._pos.y
        # where the object's height extent ends on the screen
        self.y_end = self._pos.y + self._size.y

    def __str__(self): 
        return f'Bounds(maxWidth={self._size}, pos={self._pos})'
