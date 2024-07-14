
from enum import Enum
from typing import List

from ._interfaces import ColliderInterface, ObjectInterface

class ColliderFill(Enum):
    FILLED = 1
    HOLLOW = 2


class Collider(ColliderInterface):
    def __init__(self, colliderFill: ColliderFill):
        
        # a list of the objects the collier has collided with
        self._collisions: List[CollisionData] = []

        super().__init__(colliderFill)

    def collide_with(self, other: ObjectInterface, collisionType: 'CollisionType'):
        self._collisions.append(CollisionData(other, collisionType))


class CollisionType(Enum):
    ''''
     Holds the different ways a collision can be interpreted
    '''
    START = 1
    CONTINUING = 2
    END = 3

class CollisionData:
    def __init__(self, object: ObjectInterface, collisionType: CollisionType):
        self.object = object
        self.collisionType = collisionType