import time

class FrameTimeKeeper:
    '''
    Holds the time past since the last frame
        - Used to get the delta_time, milliseconds, which is the time past since the last frame.
    Holds the time since the start of the game
    '''
    delta_time: float = 0

    def __init__(self):

        self.dt_count_start: float = 0
        self.dt_count_end: float = 0

    @property
    def frame_rate(self):
        '''
        Calculates and updates the frame rate of the game
        - The frame rate is the number of times per second that the game is being updated
        - This calculation is based on the delta time of every frame
        '''
        # calculate the frame rate
        return 1000 / self.delta_time
    
    @frame_rate.setter
    def frame_rate(self, _):
        pass


    def run(self):
        '''
        Marks the start of another game loop

        '''
        # get the end of the last loop
        # if this isn't the first loop of the game
        self.dt_count_end = time.time() if self.dt_count_start!= 0 else self.dt_count_start

        # calculate delta time, convert to milliseconds
        self.delta_time = float((self.dt_count_end - self.dt_count_start) * 1000)

        # mark the start of the next loop
        self.dt_count_start = time.time()

