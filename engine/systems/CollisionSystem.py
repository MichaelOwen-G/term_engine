from typing import List

from ..engine_interface import EngineInterface

from ..panel._interfaces import PanelInterface
from ..components._interfaces import ColliderInterface
from ..systems._interfaces import ObjectSystem

from ..components.collider import ColliderFill


class CollisionSystem(ObjectSystem):
    def __init__(self, game_engine: EngineInterface):
        super().__init__(game_engine)

    def run(self, dt: float, object: ColliderInterface):
        self.check_collisions(object, self.game_engine.collidable_objects)

    def check_collisions(self, colliderObject: ColliderInterface, objects: List[ColliderInterface]):
        ''' Checks the collisions of an object with all the other objects '''
        # clear all collisions
        colliderObject.clear_collisions()

        # iterate thru all the objects
        for other in objects:
            # if colliderObject is FILLED
            # check if other object is within the bounds of the collider
            if colliderObject.colliderFill == ColliderFill.FILLED:
                if self.are_within_bounds(object):
                    colliderObject.collide_with(object)

             # if colliderObject is HOLLOW
            else:
                # check if the object is only touching the borders of the colliderObject and 
                # not the inside the colliderObject
                if self.are_only_touching_borders(object):
                    colliderObject.collide_with(object)


    def are_within_bounds(self, colliderObject: PanelInterface, object: PanelInterface) -> bool:
        '''
        Checks if the object is within the bounds of possible collision of the colliderObject
        '''

        collided: bool = False

        # get the furthest point on the top area of the colliderObject that the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_y_start: int = colliderObject.bounds.y_start - object.size.y

        # get the furthest point on the bottom area of the colliderObject that the end of the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_y_end: int = colliderObject.bounds.y_end + object.size.y

        # get the furthest point on the left area of the colliderObject that the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_x_start: int = colliderObject.bounds.x_start - object.size.x

        # get the furthest point on the right area of the colliderObject that the object's end can be 
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_x_end: int = colliderObject.bounds.x_end + object.size.x

        # check if the object is within the bounds of furthest points of possible collision
        if (furthest_collision_point_x_start <= object.bounds.x_start):
            if (furthest_collision_point_x_end >= object.bounds.x_end):
                if (furthest_collision_point_y_start <= object.bounds.y_start):
                    if (furthest_collision_point_y_end >= object.bounds.y_end):
                        collided = True
            
            
        return collided

    def are_only_touching_borders(self, colliderObject: PanelInterface, object: PanelInterface) -> bool:
        '''
        Checks if the object is touching the collider
        '''

        collided: bool = False

        # check if the object is collding with the colliderObject
        if (self.are_within_bounds(colliderObject, object)): collided = True

        # check if the object is fully inside the colliderObject
        # check if the width bounds of the object are inside those of colliderObject
        if (object.bounds.x_start >= colliderObject.bounds.x_start and object.bounds.x_end <= colliderObject.bounds.x_end):
            # check if the height bounds of the object are inside those of colliderObject
            if (object.bounds.y_start >= colliderObject.bounds.y_start and object.bounds.y_end <= colliderObject.bounds.y_end):
                collided = False

        return collided

