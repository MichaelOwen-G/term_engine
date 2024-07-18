'''
Enables stacking of multiple drawing objects in an ordered manner

'''

from typing import List
from enum import Enum


from ._interfaces import DrawingInterface, DrawingStackInterface
from .drawing import Drawing

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
    
    @max_state.setter
    def max_state(self, _):
        pass


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

        print(f'------ Set {drawing.tag} local pos to y: {posY}')
        print(f'------ In Self Constraints w:{self.maxWidth}, h:{self.maxHeight}')

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

        print(f'---- Updating Stack Constraints ::::::::')
        print(f'------ Stack Direction: {stackDirection}')

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
        print(f'------ Updated Self {self.tag} Constraints w:{self.maxWidth}, h:{self.maxHeight}')

