from abc import ABC, abstractmethod

from term_engine.panel.frame_buffer import FrameBuffer

from term_engine.metrics.bounds import Bounds
from term_engine.metrics.vec2 import Vec2

class PanelInterface(ABC):
    '''
        Defines the interface for a panel object
    '''
    def __init__(self):
        # Has Measurements
        self.pos: Vec2 = None
        ''' position on the screen: Vec2'''
        self.size: Vec2 = None
        ''' Size of the panel: Vec2'''
        self.priority: int = None
        ''' Priority of the panel: int'''
        self.bounds: Bounds = None
        ''' Bounds of the panel: Bounds'''

        # Utilizes curses and curses.panel
        self.panelWindow = None
        ''' curses.panel window '''
        self.panel = None
        ''' curses.panel object '''
        self.key_pressed: int = None
        ''' Key Pressed in on the panel: int '''

        # Uses double buffering to render the frames

    ''' MUST HAVE THE FOLLOWING INSTRUCTIONS'''
    ''' Should Have Update'''
    @abstractmethod
    def update(self, dt: int, drawing) -> None:
        ''' Updates the panel'''
        pass

    @abstractmethod
    def redrawWindow(self) -> None:
        ''' Redraws/Renders the panel '''
        pass

    @abstractmethod
    def shouldRedraw(self):
        pass
        