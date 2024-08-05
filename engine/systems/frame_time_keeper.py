import time

from ._interfaces import EngineSystem

class FrameTimeKeeper(EngineSystem):
    '''
    Holds the time past since the last frame
        - Used to get the delta_time, milliseconds, which is the time past since the last frame.
    Holds the time since the start of the game
    '''
    delta_time: float = 0

    def __init__(self, game_engine):
        
        self.game_engine = game_engine

        self.dt_count_start: float = 0
        self.dt_count_end: float = 0

        super().__init__()

    @property
    def fps(self):
        '''
        Calculates and updates the frame rate of the game
        - The frame rate is the number of times per second that the game is being updated
        - This calculation is based on the delta time of every frame
        '''
        # calculate the frame rate
        # convert delta_time ms to secs and
        # divide 1 by the result
        return 1000 / self.delta_time if self.delta_time!= 0 else 0
    
    @fps.setter
    def fps(self, _):
        pass


    def run(self, game_engine):
        '''
        Marks the start of another game loop

        '''
        # get the end of the last loop
        # if this isn't the first loop of the game
        self.dt_count_end = time.time() if self.dt_count_start!= 0 else self.dt_count_start

        # calculate delta time/time passed, convert to milliseconds
        self.delta_time = float((self.dt_count_end - self.dt_count_start) * 1000)

        # mark the start of the next loop
        self.dt_count_start = time.time()

        self._limit_frames_to_cap()

        

    def _limit_frames_to_cap(self):
        # # get preferred delta time accoring to game.frame_cap
        self._pref_dt = 1 / self.game_engine.frame_cap

        # # check if this frame's delta_time was longer than pref_dt
        # # if so ignore limit_frames_to_cap
        # if self.delta_time >= self._pref_dt: return

        # # if not time.sleep the remaining time
        time.sleep(self._pref_dt)

        # time.sleep(.005)
