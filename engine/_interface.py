from abc import ABC, abstractmethod


class EngineInterface(ABC):
    '''
    Defines the interface for the game engine
    '''
    def __init__(self, window_width: int, window_height: int, debug_mode: bool):
        ''' MUST HAVE THE FOLLOWING FIELDS'''
        self.frame_time_keeper = None

        self.rendering_system = None
        
        self.collision_system = None

        self.typing_system = None

        self.engine_systems = None
        
        self.engine_effects: list = []

        self.objects: list = []

        self.debug_mode: bool = debug_mode

        '''METRICS'''
        self.window_width = window_width
        self.window_height = window_height

        self.floor = self.window_height - 2
        self.roof = 1

        # UTILIZES curses
        self.stdscr = None

        ''' MUST HAVE THE FOLLOWING METHODS'''
        @abstractmethod
        def run(self): pass