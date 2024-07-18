
from typing import override
from engine.effects.repeat_effect import RepeatEffect, RepeatType
from engine.metrics.duration import Duration


class AudioEffect(RepeatEffect):
    def __init__(self, repeatType: RepeatType = RepeatType.ONCE_IN_NEXT_FRAME, duration: Duration = None):

        self._playing: bool = False

        super().__init__(repeatType, duration)


    @property
    def playing(self):
        return self._playing
    
    @playing.setter
    def playing(self, _):
        pass

    @override
    def shouldRun(self, dt: float) -> bool:
        return super().shouldRun(dt) if self._playing else False


    def load(self, filepath):
        # load the audio from file
        self.file_path: str = filepath

    
    def play(self):
        self._playing = True

    def pause(self):
        self._playing = False

    def stop(self):
        # pause audio
        self.pause()

        # delete audio
        self.dispose()

    def dispose(self):
        pass