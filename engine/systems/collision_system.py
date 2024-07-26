from typing import List

from .._interface import EngineInterface

from ..panel._interfaces import PanelInterface
from ..components._interfaces import ColliderInterface
from ._interfaces import ObjectSystem

from ..components.collider import ColliderFill, CollisionType


class CollisionSystem(ObjectSystem):
    def __init__(self, game_engine: EngineInterface):
        super().__init__(game_engine)

    def run(self, my_object: ColliderInterface):
        print(f'CHECKING COLLISIONS FOR: {my_object.tags}')
        print(f'IN OBJECTS: {self.game_engine.collidable_objects}')
        
        self.check_collisions(my_object, self.game_engine.collidable_objects)

    def check_collisions(self, my_object: ColliderInterface, objects_can_collide: List[ColliderInterface]):
        ''' Checks the collisions of an object with all the other objects '''
        # clear all collisions
        my_object.clear_collisions()

        # iterate thru all the objects that can collide with my_object
        for other in objects_can_collide:
            if other is my_object: continue
            
            # if colliderObject is FILLED
            # check if other object is within the bounds of my_object
            if my_object.colliderFill == ColliderFill.FILLED:
                print(f'COLLIDER IS FILLED')
                if self.are_within_bounds(my_object, other):
                    print(f'COLLIDED WITH {other.tags}')
                    my_object.collide_with(other, CollisionType.CONTINUING)

             # if colliderObject is HOLLOW
            else:
                print(f'COLLIDER IS HOLLOW')
                # check if the object is only touching the borders of the colliderObject and 
                # not the inside the colliderObject
                if self.are_only_touching_borders(my_object, other):
                    print(f'COLLIDED WITH {other.tags}')
                    my_object.collide_with(other, CollisionType.CONTINUING)


    def are_within_bounds(self, colliderObject: PanelInterface, other: PanelInterface) -> bool:
        '''
        Checks if the object is within the bounds of possible collision of the colliderObject
        '''

        collided: bool = False

        # get the furthest point on the top area of the colliderObject that the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_y_start: int = colliderObject.bounds.y_start - other.size.y

        # get the furthest point on the bottom area of the colliderObject that the end of the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_y_end: int = colliderObject.bounds.y_end + other.size.y

        # get the furthest point on the left area of the colliderObject that the object can be
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_x_start: int = colliderObject.bounds.x_start - other.size.x

        # get the furthest point on the right area of the colliderObject that the object's end can be 
        # and still be within the colliderObject's bounds or can be possibly colliding with the colliderObject
        furthest_collision_point_x_end: int = colliderObject.bounds.x_end + other.size.x

        # check if the object is within the bounds of furthest points of possible collision
        if (furthest_collision_point_x_start <= other.bounds.x_start):
            if (furthest_collision_point_x_end >= other.bounds.x_end):
                if (furthest_collision_point_y_start <= other.bounds.y_start):
                    if (furthest_collision_point_y_end >= other.bounds.y_end):
                        collided = True
            
            
        return collided

    def are_only_touching_borders(self, my_object: PanelInterface, other: PanelInterface) -> bool:
        '''
        Checks if the object is touching the collider
        '''

        collided: bool = False

        # check if the object is collding with the colliderObject
        if (self.are_within_bounds(my_object, other)): collided = True

        # check if the object is fully inside the colliderObject
        # check if the width bounds of the object are inside those of colliderObject
        if (other.bounds.x_start >= my_object.bounds.x_start and other.bounds.x_end <= my_object.bounds.x_end):
            # check if the height bounds of the object are inside those of colliderObject
            if (other.bounds.y_start >= my_object.bounds.y_start and other.bounds.y_end <= my_object.bounds.y_end):
                collided = False

        return collided

