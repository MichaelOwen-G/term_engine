from typing import List, override 

from ..metrics.vec2 import Vec2

from ._interfaces import DrawingInterface


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

        # to store lists of lines for multiple states of the drawing
        # 2D list
        self.states: list[list[str]] = []

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