from typing import List, override
import time

from term_engine.components.object import ColliderFill, CollisionType

from term_engine.panel._interfaces import PanelInterface
from term_engine.components._interfaces import ColliderInterface
from term_engine.systems._interfaces import ObjectSystem, EngineSystem


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


'''                              OBJECT SYSTEMS             '''

class RenderingSystem(ObjectSystem):
    '''
        Responsible for rendering the Object's panels on the screen
    '''

    def run_all(self):
        game_objs = self.game_engine.objects

        for obj in game_objs:
            self.run(obj)

    def run(self, object: PanelInterface, game_engine):
        '''
        Rerenders/Redraws the front buffer of an object's panel to the screen
        '''
        # redraw/rerender the object's panels if the object wants to redraw 
        if object.shouldRedraw(): 
            object.render(game_engine)
        
    def with_priority(self, objects: list[PanelInterface]) -> list[PanelInterface]:
        ''' Rearrange objects with their priority'''
        stacked_objs: list[PanelInterface] = []
        
        # get all the priorities
        priorities: list[int] = [obj.priority for obj in objects]
        
        priorities.sort() # sort them
        
        # add the objects with their sorted priorities
        for pr in priorities:
            stacked_objs.extend([obj for obj in objects if obj.priority == pr])
        
        return stacked_objs
    

class CollisionSystem(ObjectSystem):
    def __init__(self):
        super().__init__()

    def run(self, my_object: ColliderInterface, game_engine):
        print(f'CHECKING COLLISIONS FOR: {my_object.tags}')
        print(f'IN OBJECTS: {game_engine.collidable_objects}')
        
        self.check_collisions(my_object, game_engine.collidable_objects)

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
    
        ''' ANOTHER WAY TO DO THIS
        # since the objects are quadilaterals, 
        # a collison means that one or more of the four points of the smaller object,
        # is within the bounds of the bigger object
        
        # determine the bigger and smaller object
        # bigger object
        bigger = colliderObject if colliderObject.bounds.bigger_than(other) else other
        
        # smaller object
        smaller = other if bigger == colliderObject else other
        
        # using the smaller object,
        # check whether its four points are within the bounds of the bigger object
        
        return True if smaller.bounds.is_within(bigger) else False
        '''

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

