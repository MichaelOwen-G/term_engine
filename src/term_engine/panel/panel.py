import curses
import curses.panel
from typing import override

from term_engine.panel.frame_buffer import FrameBuffer

from term_engine.panel._interfaces import PanelInterface
from term_engine.components._interfaces import DrawingInterface, DrawingStackInterface

from term_engine.metrics.bounds import Bounds
from term_engine.metrics.vec2 import Vec2

#panel object
class Panel(PanelInterface):
    '''
    Handles operations for the window or canvas that is being rendered on the screen
    - It is based on the curses.panel.panel object
    - It takes its constraints from the objects constraints
    - It uses double buffering to render the frames of the drawing object
    '''
    
    def __init__(self, size: Vec2, pos: Vec2, priority: int = 0):
        super().__init__()
        
        # set the constraints, position and priority of the panel
        self.size = Vec2(size.x, size.y)
        self.pos = pos
        self.priority = priority

        self.keys_pressed:list = []

        # create the panel window with constraints
        # self.createPanelWindow(self.size, self.pos)

        # initialize double buffering for the panel
        # back buffer stores the previous frame of the panel
        self._back_buffer: FrameBuffer = FrameBuffer(size = size)

        # front buffer stores the current frame of the panel
        self._front_buffer: FrameBuffer = FrameBuffer(size = size)

        # define bounds of the panel
        self.bounds: Bounds = Bounds(size, pos)

        # print('INITIAL BUFFER', self._front_buffer.buffer)
    
    ''' SETTERS AND GETTERS FOR PROPERTIES '''
    @property
    def position(self) -> Vec2:
        ''' Returns the position of the panel '''
        return self.pos
    
    @position.setter
    def position(self, position: Vec2) -> None:
        ''' Sets the position of the panel '''
        # get direction of movement
        dir: Vec2 = position - self.pos

        # move towrads dir
        self.move(dir)

    @property
    def front_buffer(self) -> str:
        ''' Returns front_buffer class as a string '''
        return self._front_buffer.in_pixels()
    
    @front_buffer.setter
    def front_buffer(self):
        ''' Can't set the front buffer with setter'''
        pass

    ''' OVERRIDES FOR PANEL INTERFACE '''
    @override
    def update(self, dt: int, drawing):
        '''
        - This method is called every frame.
        - Updates the panel class with the given drawing
            - Gets the current frame of the drawing
            - Creates a front buffer from the current frame of the drawing
            - The front buffer is what will be rendered on the panel
            - Pushes the previous frame to the back buffer
        '''

        print(f'---- panel update ----')

        # validate the drawing object is of type Drawing/DrawingStack, throw error if not
        if not (isinstance(drawing, DrawingInterface) or isinstance(drawing, DrawingStackInterface)):
            raise TypeError("drawing must be of type Drawing or DrawingStack")
        
        # clear the back buffer to start manipulating it on this frame
        self._back_buffer.clear()
        
        # manipulate the back buffer with current drawing
        self._back_buffer.manipulateBufferWithDrawing(drawing)

        print('BUFFER AFTER UPDATE', self._back_buffer._buffer)


    @override
    def redrawWindow(self) -> None:
        '''
            Redraws/Renders and refreshes this panel_window on the screen with the front_buffer
        '''

        # push the back buffer to the front buffer
        self._front_buffer.copy(self._back_buffer)

        if not self.panel_window_exists(): return None
        
        self.panelWindow.addstr(0,0, self.front_buffer)
        self.panelWindow.refresh()

    def reposition_window(self):
        # clear front buffer
        self._front_buffer.clear()

        self.rebuild_window(self.size, self.pos)

    @override
    def shouldRedraw(self) -> bool:
        '''
        Checks if the panel window needs to be redrawn
        '''
        # redraw if the front buffer has been updated
        return not self._front_buffer.isEqualTo(self._back_buffer) # True if the two buffers are not equal
    
    def panel_window_exists(self) -> bool: return self.panelWindow != None


    ''' WINDOW MANIPULATION (CRUD OPERATIONS ON PANEL WINDOWS) '''
    def createPanelWindow(self, size: Vec2, pos: Vec2) -> None:
        '''
        Creates a panel window for an object in the CLI with the given size and position
        '''
        # print('SIZE WHEN CREATING PANEL WINDOW', size)
        self.panelWindow = curses.newwin( size.y , size.x + 1, pos.y, pos.x)
        self.panel = curses.panel.new_panel(self.panelWindow)

        # set no delay to key press getting
        self.panelWindow.nodelay(True)

        # intialize key_pressed to empty key stroke
        self.key_pressed = -1

        if self.listen_to_keys: 
            self.panelWindow.keypad(True)
            self.panelWindow.nodelay(True)

        self.panelWindow.refresh()

    def rebuild_window(self, size, pos):
        ''' Pop and recreate the panel window '''
        self.destroyWindow()
        self.createPanelWindow(size, pos)
    
    def destroyWindow(self):
        '''
        Pops the panel window off the stack
        - This is used when the panel is no longer needed
        '''
        if not self.panel_window_exists(): return
            
        self.panelWindow.clear()

        self.panelWindow.refresh()
        self.panelWindow = None

    ''' KEY SCANNING / TYPING '''
    def scan_key(self) -> int:
        ''' Gets the key pressed '''
        if not self.panel_window_exists(): return -1

        return self.panelWindow.getch() if self.listen_for_key_press() else -1
    
    def listen_for_key_press(self) -> bool: return False


class StaticPanel(Panel):
    '''
    A panel that does not update
    - Its update method runs once
    - 
    '''
    def __init__(self, size: Vec2, pos: Vec2, priority: int = 0):
        self.built = False
        super().__init__(size, pos, priority)

    def update(self, dt: int, drawing):
        # run once
        if not self.built:
            self.built = True
            return super().update(dt, drawing)

    def shouldRedraw(self) -> bool:
        return False if self.built else super().shouldRedraw()

