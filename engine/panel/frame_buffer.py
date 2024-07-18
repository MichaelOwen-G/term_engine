import numpy as np

from ..components.drawing import Drawing
from ..components.drawing_stack import DrawingStack

from ..metrics.vec2 import Vec2


class FrameBuffer:
    '''
    Holds the frame buffer or pixels of a panel.

    - The FrameBuffer class contains a 2D array that holds the characters/pixels 
            to be rendered on the screen for each frame
    This allows the efficient updating and rendering of the screen by
        minimizing screen operations and ensuring that only changed pixels are
        rendered.
    '''
    def __init__(self, size: Vec2):
        '''
        - Receives the size of the frame buffer
        - Initializes the frame buffer to an empty 2D list of empty strings
        '''

        self.size = size

        self._emptyBuffer: list[list[str]] = self._createEmptyBuffer()

        self._buffer: list[list[str]] = self._emptyBuffer

    ''' SETTERS AND GETTERS FOR PROPERTIES '''
    @property
    def buffer(self) -> str:
        return self._buffer
    
    @buffer.setter
    def buffer(self, buffer: list[list[str]]):
        # validate input
        if not isinstance(buffer, list[list[str]]):
            raise TypeError("Buffer must be of type list[list[str]]")
        
        self._buffer = buffer

    
    def _addLinesToBuffer(self, lines: list[str], pos: Vec2) -> None:
        '''
        Adds the lines, a list of strings, to the frame buffer according to its the local position
        '''
        # print('======ADDING LINES TO BUFFER======')
        # print('LINES BEING ADDED TO BUFFER', lines)
        # print(f'BUFFER BEFORE ADDING LINES: {self._buffer}')
        # iterate through the lines
        for i in range(len(lines)):
            line: str = lines[i]
            # print(f'LINE BEING ADDED TO BUFFER [{line}]')

            # get the position of the line
            # the first line starts at top left
            # the next below it
            line_pos: Vec2 = Vec2(pos.x, pos.y + i)

            try:
                # get the line in _buffer that the newline updates
                buffer_line_chars: list[str] = self._buffer[line_pos.y]
            except IndexError:
                print(f'ERROR: ')
                print(f'While Adding the {i}th Line =>{line}<= to Buffer')
                print(f'LOCAL POS [{line_pos.y}], is trys to occupy, IS OUTSIDE LOCAL BUFFER"S BOUNDS [{self.size.y}]')
                print(f'')
                raise IndexError(
                    f'''
                        ERROR:
                            While Adding the {i}th Line =>{line}<= to Buffer
                            LOCAL POS [{line_pos.y}], is trys to occupy, IS OUTSIDE LOCAL BUFFER"S BOUNDS [{self.size.y}]
                    '''
                )

            # update the line_chars/line_pixels
            first_part = np.array(buffer_line_chars[0:line_pos.x])
            second_part = np.array([*line])
            third_part = np.array([])

            # if the line to add did not reach the end
            if not ((line_pos.x + len(line)) >= len(buffer_line_chars)):
                third_part = np.array(buffer_line_chars[line_pos.x + len(line):])

            # print('NEW LINE', new_line)

            self._buffer[line_pos.y] = np.concatenate((first_part, second_part, third_part))

            # print('NEW LINE', self._buffer[line_pos.y])

            # print('NEW BUFFER AFER LINE', self._buffer)



    def _validateDrawingInBounds(self, drawing: Drawing) -> None:
        '''
        Checks if the drawing is trying to exceed the size of the frame buffer
        '''
        # get the width the drawing is trying to occupy
        # max_width of drawing plus its x offset
        drawing_space_width: int = drawing.maxWidth
        # print('DRAWING SPACE WIDTH', drawing.maxWidth, drawing.local_pos.x)

        # get the height the drawing is trying to occupy
        # max_height of drawing plus its y offset
        drawing_space_height: int = drawing.maxHeight
        # print('DRAWING SPACE HEIGHT', drawing.maxHeight, drawing.local_pos.y)

        # print(f'DRAWING PANEL SIZE {self.size.x}, {self.size.y}')

        # validate that the line does not exceed the width of the frame buffer
        if drawing_space_width > self.size.x or drawing_space_height > self.size.y:
            raise ValueError(f"Drawing  {drawing.tag} is trying to occupy space {drawing_space_width, drawing_space_height} outside its panel's bounds ({self.size.x}, {self.size.y})")


    def manipulateBufferWithDrawing(self, drawing) -> None:
        '''
        Manipulates the buffer with the given drawing.
        - Adds the lines of the drawing to the frame buffer 
            according to the local position of the drawing
        '''
        # print()
        # print(f'DRAWING HEIGHT {self.size.y}')
        # print('======MANIPULATING BUFFER WITH DRAWING======')

        # if drawing is of the DrawingStack class
        if (isinstance(drawing, DrawingStack)):
            print('MANIPULATING BUFFER WITH DRAWING STACK: ', drawing.tag)
            # recall this function for all the drawings
            for drawing in drawing.drawings: 
                self.manipulateBufferWithDrawing(drawing)

        # if drawing is of the Drawing class
        elif (isinstance(drawing, Drawing)):
            print('MANIPULATING BUFFER WITH DRAWING: ', drawing.tag)
            print(f'local pos y: {drawing.local_pos.y}, X: {drawing.local_pos.x}')
            # validate drawing is in panel bounds
            self._validateDrawingInBounds(drawing)

            # get the current state of the drawing and add it to frame buffer
            # according to local_position of the drawing
            # print('MANIPUATING BUFFER WITH DRAWING: ', drawing.tag)
            # print('CURRENT STATE; ', drawing.get_current_state())
            self._addLinesToBuffer(drawing.get_current_state(), drawing.local_pos)
        
        else:
            raise TypeError("drawing must be of type Drawing or DrawingStack")
        
        # print('==============================================')


    def resize(self, size: Vec2):
        '''
        Resizes the frame buffer
        '''
        self.size = size

        self._emptyBuffer = self._createEmptyBuffer()

    def concentrateBuffer(self) -> str: 
        '''
        Converts the buffer pixels to a string
        '''

        return "\n".join("".join(line) for line in self._buffer)

    
    def isEqualTo(self, other: 'FrameBuffer') -> bool:
        '''
        Checks if this frame buffer is equal to the other frame buffer
        '''
        # validate input
        if not isinstance(other, FrameBuffer):
            raise TypeError("Can only Compare objects of type FrameBuffer")

        # check if the buffers are equal
        return np.array_equal(self._buffer, other._buffer)

    def clear(self): self._buffer = self._createEmptyBuffer()

    def copy(self, other: 'FrameBuffer'):
        ''' Changes this fields to other's '''

        self.size = other.size

        self._buffer = other._buffer

    def _createEmptyBuffer(self) -> list[list[str]]: 
        # print("Creating empty buffer of size ", self.size.x, "x", self.size.y)
        return np.full((self.size.y, self.size.x), ' ')

