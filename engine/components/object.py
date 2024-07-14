
from typing import override

from engine.components.collider import CollisionType

from ..engine_interface import EngineInterface
from .collider import Collider, ColliderFill
from ._interfaces import ObjectInterface, DrawingInterface

from ..effects._interfaces import Effect

from ..metrics.vec2 import Vec2
from ..panel.Panel import Panel

class Object(Panel, ObjectInterface):
    def __init__(self, tag: str = '', drawing: DrawingInterface = None, position: Vec2 = Vec2(0, 0), priority: int =0):
        ObjectInterface.__init__(self, drawing, tag)

        super().__init__(drawing.maxSize, position, priority = priority)

        self._back_position = None
        self._back_size = None
        self._back_priority = None

        
    def addEffect(self, effect: Effect):
        ''' Takes an Effect and adds it to the list of effects
            Can be RepeatEffect
            - RepeatEffect
            - RepeatCallbacksEffect
        '''
        # validate effect
        self.effects.append(effect)

    @override
    def update(self, dt: float, game: EngineInterface):
        self.update_pos_flags(game)
        super().update(dt, self.drawing)


    def check_for_new_config(self) -> bool:
        ''' Checks if the object's metrics have changed since the last time it was rendered'''
        # if back configd are empty, then the object has never been rendered before
        if (self._back_position is None or self._back_size is None): return True

        if ((self._back_position != self.position) or (self._back_size != self.size)):
            return True
        
        return False


    @override
    def shouldRerender(self) -> bool:
        ''' Returns True if the object has changed size or position (metrics have changed) and
            the object is in view or
            the object's panel needs to redraw

        '''

        # if the object has changed size or position (config has changed) 
        # the object should render no matter what, otherwise
        # the object should rerender if the objects panel needs to redraw
        # print('CHECKING FOR NEW CONFIG', self.check_for_new_config())
        # print('BACK CONFIG', self._back_position, self._back_size)
        # print('CURRENT CONFIG', self.position, self.size)
        return True if self.check_for_new_config() else self.shouldRedraw()
           
    @override
    def render(self):
        ''' Renders the object'''   
        # handle reconfiguring
        # handle repositiong and resizing of the panel_window
        if (self.check_for_new_config()): self.reconfigurePanelWindow()

        print('REDRAWING PANEL WINDOW', self.front_buffer, self.size)

        # redraw the window if the panel_window needs to redraw
        if (self.panelWindow != None): self.redrawWindow()
         
    
    def reconfigurePanelWindow(self) -> bool:
        ''' Handles the change in the metrics of the 
         - Repositiong and resizing the object's panel_window
         - Since repositioning and resizing the panel_window is weirdly non-functional in curses,
         this function is a workaround to rebuild the panel_window in the new position and size.
         The approach works but it is very costly.
        '''
        
        # the object's panel should be rendered in a fresh configs
        # pop the old panel_window if it exists
        if self.panelWindow!= None: self.destroyWindow()

        # create a new panel_window with the new configs
        # if the object is in view
        if self.in_view: self.createPanelWindow(self.size, self.pos)

        # update the back_position
        try:
            self._back_position.replace_with(self.pos)

            # update the back_size
            self._back_size.replace_with(self.size)

        except AttributeError:
            self._back_position = Vec2(self.pos.x, self.pos.y)
            self._back_size = Vec2(self.size.x, self.size.y)

        # update bounds
        self.bounds.pos = self.pos
        self.bounds.size = self.size

    def update_pos_flags(self, game: EngineInterface):
        # update the position flags
        # check against horizontal extremes of the game_window
        self.past_left_extreme = False
        self.past_right_extreme = False

        if self.position.x <= 0:
            self.past_left_extreme = True
        elif self.bounds.x_end >= game.window_width - 1:
            self.past_right_extreme = True


        self.above_roof = False
        self.below_floor = False
        self.on_floor = False
        self.on_roof = False

        # check against vertical extremes
        if self.bounds.y_end == game.floor:
            self.on_floor = True
        elif self.bounds.y_end > game.floor:
            self.below_floor = True
        elif self.bounds.y_start == game.roof:
            self.above_roof = True
        elif self.position.y < game.roof:
            self.on_roof = True

        # check if the object is in 
        self.in_view = False

        if (not self.past_left_extreme and not self.past_right_extreme) and (not self.above_roof and not self.below_floor):
            self.in_view = True
        
        print('in view', self.in_view)
   


class CollidableObject (Object, Collider):
    def __init__(
                 self, 
                 drawing, 
                 tag: str = "", 
                 position: Vec2 = Vec2(0, 0), 
                 priority: int =0, 
                 colliderFill: ColliderFill = ColliderFill.FILLED,
                 ):
        
        Object.__init__(self, drawing, tag, position, priority)
        Collider.__init__(self, colliderFill)

    def update(self, dt: float):
        super().update(dt, self.drawing)

    @override
    def collide_with(self, other: ObjectInterface, collisionType: CollisionType):
        ''' Takes another object and checks if they are colliding
        '''
        # if this is on top of the other object
        # this is on the floor
        if self.position.y + self.size.y  == other.position.y:
            self.on_floor = True

        return super().collide_with(other, collisionType)
