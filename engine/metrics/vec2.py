

class Vec2:
    '''
    Holds a 2D vector with x and y
    x and y values must be integers:
     since the curses draw func only takes integers
    Has:
    - x(int)
    - y(int)
    '''
    def __init__(self, x:int = 0, y:int = 0):
        self._x = x
        self._y = y

    '''
    Property getter and setter for x and y
    '''
    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, x: int):
        # validate the inputted x value
        x = self._validate_value(x)

        self._x = x

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, y: int):
        # validate the inputted y value
        y = self._validate_value(y)

        self._y = y


    def _validate_value(self, value: int) -> int:
        # convert to int if it is not an int
        return int(value) if value is not int else value
    
    def replace_with(self, other: 'Vec2'):
        '''
        Replace the values of this vector with the values of another vector
        '''
        self._x = other.x
        self._y = other.y
    

    '''
    Mathematical operations for vec2
    '''
    def __add__(self, other):
        '''
        Add two vectors together
        - a = Vec2(1, 2)
        - b = Vec2(3, 4)
        - a + b => Vec(4, 6)
        '''
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        '''
        Substract two vectors
        '''
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        '''
        Multiply two vectors
        '''
        return Vec2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)
    
    def __eq__(self, other):
        '''
        Equate two vectors
        '''
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        '''
        Print the vector
        '''
        return f"Vec2({self.x}, {self.y})"
    
    def __str__(self):
        '''
        Print the vector
        '''
        return f"({self.x}, {self.y})"
    
    def __neg__(self):
        '''
        Negate the vector
        '''
        return Vec2(-self.x, -self.y)
    
    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))
    
    def __bool__(self):
        '''
        Check if the vector is not 0
        '''
        return self.x!= 0 or self.y!= 0