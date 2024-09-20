from enum import Enum
from typing import List, override 

from term_engine.metrics.vec2 import Vec2

from term_engine.components._interfaces import DrawingInterface, DrawingStackInterface

class Drawing(DrawingInterface):
    '''
    Has:
        - tag(str): that ids the drawing
        - constraints: maxWidth(int), maxHeight(int)
        - local_pos(Vec2):
            the position of the drawing relative to the canvas
        - frames(list):
            with lines(list)
    '''

    def __init__(self, tag = '', drawingStates: List[str] = [], stripNewLines = True, fillBlanks = False):
        '''
        To make a drawing with multiple frames
        - Takes:
            - tag(str): the id of the drawing
        - Use the draw method to add a string representation of the drawing
        - Use can add multiple frames to the drawing by using the addFrame method
        '''
        super().__init__(tag, 0, 0)

        print()
        print(f'::::::::: DRAWING INIT :::::::::')

        # to track the constraints of the drawing
        self.maxWidth: int = 0
        self.maxHeight: int = 0

        
        # 2D list
        self.states: list[list[str]] = []
        '''
        To store lists of lines for multiple states of the drawing

        Example:
        ```python
        self.states = [
                        ["loading.",
                         "||",
                        ],
                        ["loading..",
                         "|||||",
                        ],
                        ["loading.....",
                         "||||||||||",
                        ],
                     ] 
        ```
        '''

        # the index of the current frame
        self._current_state: int = 0

        # the position of the drawing relative to the object's panel/canvas
        self.local_pos = Vec2()

        self.drawStates(drawingStates, stripNewLines, fillBlanks)

    '''
    SETTERS AND GETTERS FOR PROPERTIES
    '''
    @property
    def current_state(self) -> int:
        return self._current_state
    
    @current_state.setter
    def current_state(self, state: int):
        # validate the inputted frame value
        # if inputted frame index is out of bounds, throw error
        if state < 0 or state >= len(self.states):
            raise IndexError(f"frame index out of bounds: {state} \n valid range: 0 - {len(self.states)}")
        
        self._current_state = state

    def get_current_state(self) -> list[str]:
        ''' Gives the current state of the drawing '''
        # print('STATES: ', self.states)
        return self.states[self._current_state]

    def next_state(self):
        ''' Sets the states of all the drawings to the following state '''
        self.current_state += 1 if self._current_state < (len(self.states) - 1) else - self._current_state

    def _drawState(self, stringDrawing: str, stripNewLines: bool = True, fillBlanks: bool = False):
        '''
        Register a frame of the drawing
        Takes:
        - string(String):      
            a String that is the drawing

        - stripNewLines(bool): 
            whether to remove the starting and trailing newlines 
            especially useful in multiline comments

        - fillBlanks(bool):   
            to fill the blank spaces with a " " character
            this ensures the frame drawing is a polygon

        - It takes the string: str and splits it into lines: list[str]
        - It then removes the starting and trailing newlines if necessary
        - It then fills the blank spaces if necessary
        - It then adds the lines: list[str] to the states list
        '''
        # OUTLINE
        # split the drawing to lines
        # strip newlines if necessary
        # fill the blank spaces if necessary
        # add the lines to the states list

        print(f'---- InDrawingState {self.tag}:::: ')

        # get the multilineString lines
        drawingState_lines: list[str] = stringDrawing.split('\n')

        print(f'------ drawingState_lines: {drawingState_lines}')

        # fill the blank spaces to get a drawing that covers a uniform polygon
        # get the maximum length of the lines
        maxLength = max([len(line) for line in drawingState_lines])

        # fill the blank spaces in the lines with a " " character
        for line in drawingState_lines:
            line += " " * (maxLength - len(line))

        # # add additinal lines if the drawing_lines are less than self.maxHeight
        # if len(drawingState_lines) < self.maxHeight:
        #     for _ in range(self.maxHeight - len(drawingState_lines)):
        #         drawingState_lines.append(" " * maxLength)

        print(f'------ Added state lines: {drawingState_lines}')

        # add the frame to the frames list
        self.states.append(drawingState_lines)

    @override
    def draw(self, stringDrawing: str = "", stripNewLines: bool = True, fillBlanks: bool = False,):
        '''
        To make a single frame drawing
        Takes:
            - string(String):      
                - a String that is the drawing

            - stripNewLines(bool): 
                - to remove the starting and trailing newlines 
                - especially in multiline comments

            - fillBlanks(bool):   
                - to fill the blank spaces with a " " character
                - this ensures the drawing is a polygon
        '''
        print()
        print(f'DRAWING {self.tag} STARTED:::::')

        # strip newlines for state if necessary
        # strip newlines for every state if necessary
        if stripNewLines:
            stringDrawing.strip('\n')
        
        print(f'--STRIPPED DRAWING: |{stringDrawing}|')

        # set maximum constraints of the drawing
        self._setMaxConstraints([stringDrawing])

        # make the frame
        self._drawState(stringDrawing, stripNewLines = stripNewLines, fillBlanks=fillBlanks)

        print(f'--DRAWING STATES: {self.states}')

        return self

    
    def drawStates(self, states: List[str], stripNewLines = True, fillBlanks = False):
        '''
        To make a drawing with multiple frames
        - Takes:
            - frames: a list os Strings that are the drawing
        '''
        
        print(f'-- DRAWING {self.tag} States Started :::::')
        print(f'-- DRAWING {self.tag} States: {states}')

        # strip newlines for every state if necessary
        if stripNewLines:
            states = [state.strip('\n') for state in states if state != '']
        
        # set maximum constraints of the drawing
        self._setMaxConstraints(states)

        # draw every frame
        for state in states:
            self._drawState(
                state,
                stripNewLines = stripNewLines,
                fillBlanks = fillBlanks,
                )

        print(f'--DRAWING States: {self.states}')


    def _getMaxWidth(self, states: list[str]) -> int:
        maxWidth = 0

        #iterate through the states
        for state in states:
            # get state lines
            lines: list[str] = state.split("\n")

            # get the line in state with the greatest length
            for line in lines:
                if len(line) > maxWidth:
                    maxWidth = len(line)

        # return the maximum width of the frames
        return maxWidth
    
    def _getMaxHeight(self, states: list[str]) -> int:
        maxHeight = 0

        #iterate through the states of the drawing
        for state in states:
            # get state lines
            lines: list[str] = state.split("\n")
            # get the state with the most lines
            if len(lines) > maxHeight: maxHeight = len(lines)

        # return the height of the frames
        return maxHeight
    
    def _setMaxConstraints(self, states: list[str]):
        print('STATES: ', states)
        # set max width
        self.maxWidth = self._getMaxWidth(states)

        # set max height
        self.maxHeight = self._getMaxHeight(states)

        print(f'----DRAWING CONSTRAINTS: w:{self.maxWidth}, h:{self.maxHeight}')
        

    def copy(self):
        # create a new drawing with the same tag and constraints
        # reset all the variables to their default values
        copy_of_self = Drawing(tag = self.tag)
        copy_of_self.maxWidth = self.maxWidth
        copy_of_self.maxHeight = self.maxHeight
        copy_of_self.states = self.states
        
        return copy_of_self
    
'''
Enables stacking of multiple drawing objects in an ordered manner

'''


class StackDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class DrawingStack( DrawingStackInterface, DrawingInterface):

    def __init__(self, tag: str = "", maxWidth:int = 0, maxHeight:int = 0):
        DrawingInterface.__init__(self, tag, maxWidth, maxHeight)
        DrawingStackInterface.__init__(self)

        self._current_state: int = 0

        print()
        print(f'::::::::: DRAWING STACK INIT :::::::::')

    '''
    SETTERS AND GETTERS FOR PROPERTIES
    '''
    @property
    def current_state(self) -> int:
        return self._current_state
    
    @current_state.setter
    def current_state(self, state: int) -> None:
        ''' - It switches the current state of the DrawingStack to the inputted state 
            - Inputing a state that is out of bounds will not throw an error but instead:
               set the current state of all the drawings to their last state
        '''
        # validate the inputted frame value
        # if inputted frame index is out of bounds, throw error

        self._current_state = 0
        
        for drawing in self.drawings:
            drawing_states = len(drawing.states)

            if state + 1 > drawing_states:
                drawing.current_state = (drawing_states - 1)
            else:
                drawing.current_state = state

            if drawing.current_state > self.current_state:
                self._current_state = drawing.current_state

            # print(f"drawing: {drawing.tag}, state: {drawing.current_state}")

    @property
    def max_state(self):
        ''' the highest state index all the drawings in the stack can reach '''
        return max([len(drawing.states) for drawing in self.drawings])


    def next_state(self):
        ''' Sets the states of all the drawings to the following state '''

        # get max state
        max_state = self.max_state

        # get next state index
        next_state = self._current_state + 1 if self._current_state + 1 < max_state else 0

        # set next state
        self.current_state = next_state


    ''' OVERRIDE'''
    def add(self, drawing: DrawingInterface, 
            stackDirection: StackDirection = StackDirection.VERTICAL) -> None:
        '''
        Adds the drawing to the stack
        - With StackDirection and StackAlignment

        Example:
          ```python
          arrowHead = Drawing("arrowHead")
          arrowHead.draw('>')

          arrowBody = Drawing("arrowBody")
          arrowBody.draw('--')
 
          arrowDrawing = DrawingStack(maxHeight = 3)
          arrowDrawing.add(arrowBody)

          Case 1: StackDirection.HORIZONTAL
          arrowDrawing.add(arrowHead, 
                            stackDirection=StackDirection.HORIZONTAL
                            )
          \'''
          -->

  
          \'''


          arrowDrawing = DrawingStack(maxWidth = 3)
          arrowDrawing.add(arrowBody)

          Case 2: StackDirection.VERTICAL
          arrowDrawing.add(arrowHead, 
                            stackDirection=StackDirection.VERTICAL, 
                            alignment=StackAlignment.START,
                            )
          \'''
          --'
          >'' 
          \'''
          ```

        - if the stackDirection is StackDirection.HORIZONTAL, the drawing will be added to the end of the width
        - if the stackDirection is StackDirection.VERTICAL, the drawing will be added to the end of the height
        '''
        
        print()
        print(f'-- ADDING DRAWING {drawing.tag} To the Stack ::::::::')

        # set the drawing's local position
        drawing = self._setDrawingLocalPos(drawing, stackDirection)

        #update the maxWidth && maxHeight if necessary
        self._updateStackConstraints(drawing, stackDirection)

        # add drawing to stack
        self.drawings.append(drawing)

        # set attribute to use to get the drawing        
        self._setDrawingAsAttribute(drawing)


    def _setDrawingLocalPos(self, drawing: Drawing, stackDirection: StackDirection) -> Drawing:
        '''
        Sets the drawing's local position
        '''
        print(f'---- ****************Setting Local Position of {drawing.tag} ::::::::')
        print(f'---- size of drawing: {drawing.maxWidth, drawing.maxHeight}')
        print(f'size of self {self.maxWidth, self.maxHeight}')

        # print(f'DRAWING {drawing.tag} SIZE: {drawing.maxWidth, drawing.maxHeight}')
        # get the last drawing in the stack
        
        
        # set the localPosition of the drawing in the stack
        if stackDirection == StackDirection.HORIZONTAL:
            # place x pos at the end of the row if stacking in the horizontal direction
            posX: int = 0 
            if len(self.drawings) >  1:
                lastDrawing = self.drawings[-1]

                posX: int = lastDrawing.local_pos.x + lastDrawing.maxWidth

            # set the local_pos
            drawing.local_pos.x = posX
        elif stackDirection == StackDirection.VERTICAL:
            # place y pos at the end of the column if stacking in the vertical direction
            posY: int = 0 

            if len(self.drawings) >=  1:
                lastDrawing = self.drawings[-1]

                posY: int = lastDrawing.local_pos.y + lastDrawing.maxHeight

            drawing.local_pos.y = posY

        # print(f'------ Set {drawing.tag} local pos to y: {posY}')
        # print(f'------ In Self Constraints w:{self.maxWidth}, h:{self.maxHeight}')

        return drawing
        
    
    def _setDrawingAsAttribute(self, drawing: Drawing) -> None:
        '''
        Sets the drawing as an attribute of the DrawingStack
        '''
        # if tag is empty, raise an exception
        if drawing.tag == "":
            pass
        else:
            # set attribute to use to get the drawing
            setattr(self, drawing.tag, drawing)


    def _updateStackConstraints(self, drawing: Drawing, stackDirection: StackDirection) -> None:
        #update the maxWidth && maxHeight if necessary
        
        # print(f'ADDING DRAWING [{drawing.tag}] TO STACK')
        # print(f' DRAWING {drawing.tag} SIZE: {drawing.maxWidth, drawing.maxHeight}')
        # print(f' SELF {self.maxWidth, self.maxHeight}')

        # print(f'---- Updating Stack Constraints ::::::::')
        # print(f'------ Stack Direction: {stackDirection}')

        if stackDirection == StackDirection.HORIZONTAL:
            # print(f'   ADDING WIDTH TO SELF')
            # print(f'   CHECKING HEIGHT INCR')
            self.maxWidth += drawing.maxWidth
            self.maxHeight = drawing.maxHeight if drawing.maxHeight > self.maxHeight else self.maxHeight
        else:
            # print(f'   ADDING HEIGHT TO SELF')
            # print(f'   CHECKING WIDTH INCR')
            self.maxHeight += drawing.maxHeight
            self.maxWidth  = drawing.maxWidth if drawing.maxWidth > self.maxWidth else self.maxWidth

        # print(f' UPDATED SELF: {self.maxWidth, self.maxHeight}')
        # print(f'------ Updated Self {self.tag} Constraints w:{self.maxWidth}, h:{self.maxHeight}')

