from typing import override
from ..systems._interfaces import EngineSystem

class GarbageCollectionSystem(EngineSystem):
    @override
    def run(self, game_engine):
        # find all game objects that are marked garbage
        # and delete them
        for object in game_engine.objects:
            # skip objects that are not garbage
            if not object.isGarbage: continue

            # delete garbage ones
            object.dispose()
            game_engine.game_screen.objects.remove(object)
            del object
