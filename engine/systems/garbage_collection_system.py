

from typing import override
from ..systems._interfaces import EngineSystem


class GarbageCollectionSystem(EngineSystem):
    def __init__(self, game_engine):
        super().__init__(game_engine)

    @override
    def run(self):
        # find all game objects that are marked garbage
        # and delete them
        for object in self.game_engine.objects:
            # skip objects that are not garbage
            if not object.isGarbage: continue

            # delete garbage ones
            object.dispose()
            self.game_engine.objects.remove(object)
