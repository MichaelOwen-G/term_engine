
from typing import override
from engine._interface import EngineInterface
from engine.components._interfaces import ObjectInterface
from engine.effects.repeat_effect import RepeatEffect, RepeatType
from engine.metrics.duration import Duration

import playsound

class SoundEffect(RepeatEffect):
    def __init__(self, filepath, repeatType: RepeatType = RepeatType.ONCE_IN_NEXT_FRAME, duration: Duration = None, autoPlay = True):

        self._play: bool = autoPlay

        self.filepath = filepath

        super().__init__(repeatType, duration)

    @override
    def shouldRun(self, dt: float) -> bool:
        # return False if _play is False otherwise,
        # return whether the effect should run based on repeatType and Duration
        return super().shouldRun(dt) if self._play else False

    def run(self, dt: float, game: EngineInterface, object: ObjectInterface | None):
        # play sound
        self._playfile()

        return super().run(dt, game, object)

    def _playfile(self):
        playsound.playsound(self.filepath, block = False)

    def play(self):
        self._play = True

    def pause(self):
        self._play = False

    def stop(self):
        # pause audio
        self.pause()

        # delete audio
        self.dispose()

    def dispose(self):
        
        return super().dispose()