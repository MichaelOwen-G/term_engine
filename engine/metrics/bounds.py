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
        
    @property
    def top_left(self) -> Vec2:
        ''' Returns the top left corner of the bounds '''
        return self._pos
    
    @property
    def top_right(self) -> Vec2:
        ''' Returns the top right corner of the bounds '''
        return Vec2(self._pos.x + self._size.x + 1, self._pos.y)
    
    @property
    def bottom_left(self) -> Vec2:
        ''' Returns the bottom left corner of the bounds '''
        return Vec2(self._pos.x, self._pos.y + self._size.y + 1)
    
    @property
    def bottom_right(self) -> Vec2:
        ''' Returns the bottom right corner of the bounds '''
        return Vec2(self._pos.x + self._size.x + 1, self._pos.y + self._size.y + 1)

    def _define_bounds(self):
        # where the object's width extent starts on the screen
        self.x_start = self._pos.x
         # where the object's width extent ends on the screen
        self.x_end = self._pos.x + self._size.x + 1
        # where the object's height extent starts on the screen
        self.y_start = self._pos.y
        # where the object's height extent ends on the screen
        self.y_end = self._pos.y + self._size.y + 1
        
    def is_within(self, other: 'Bounds'):
        ''' Return if this bounds is within the other '''
        # or
        if other.covers_pos(self.top_left): return True
        if other.covers_pos(self.bottom_right): return True 
        if other.covers_pos(self.top_right): return True
        if other.covers_pos(self.bottom_left): return True
        
        return False
        
    def covers_pos(self, pos: Vec2) -> bool:
        ''' Return if pos is within this bounds '''
        if pos.x <= self.x_end and pos.x >= self.x_start:
            if pos.y <= self.y_end and pos.y >= self.y_start:
                return True
        
        return False
    
    def bigger_than(self, other: 'Bounds')-> bool:
        ''' Return if this bounds is bigger than the other '''
        if self._size.x >= other.size.x and self._size.y >= other.size.y:
            return True

    def __str__(self): 
        return f'Bounds(maxWidth={self._size}, pos={self._pos})'
