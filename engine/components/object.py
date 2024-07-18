from typing import override

from ..components.collider import CollisionType

from .._interface import EngineInterface
from .collider import Collider, ColliderFill
from ._interfaces import ObjectInterface, DrawingInterface

from ..effects._interfaces import Effect

from ..metrics.vec2 import Vec2
from ..panel.panel import Panel

class Object(Panel, ObjectInterface):
    '''
    # Inheriting this class 
    - Init of class requires following methods
        - tag: str = ''
        - drawing: DrawingInterface = None  # required 
        - position: Vec2 = Vec2(0, 0)
        - priority: int =0

    ## Methods that can be overriden

    ### 1. update method
    - Called on the object at every frame


    ```python
     @override
     def update(self, dt: float, game: EngineInterface) -> None:
        super().update(self, dt: float, game: EngineInterface)

    
    ### 2. onMount method
    - Called once when the object is added into the game


    ```python
     @override
     def onMount(self) -> None:
        super().onMount(self)


    ```

    ### 3. render method
    - Called if the object's shouldRender() method is True 
    - It renders the panel on the screen

    ```python
     @override
     def render(self, game: EngineInterface) -> None:
        super().render(self, game: EngineInterface)


    ```

    ### 4. shouldRerender method
    - Called every frame to check if the object should render again

    ```python
     @override
     def shouldRerender(self) -> bool:
        return super().render(self)


    ```

    ### 5. dispose 
    - Called when the object is being deleted

    ```python
     @override
     def disposed(self) -> None:
        super().dispose(self)


    ```

    '''
    def __init__(self, tags: list[str] = [''], drawing: DrawingInterface = None, position: Vec2 = Vec2(0, 0), priority: int =0):
        ObjectInterface.__init__(self, drawing, tags)

        super().__init__(drawing.maxSize, position, priority = priority)

        # To keep track of the metrics
        self._back_position = None
        self._back_size = None
        self._back_priority = None
 
    def addEffect(self, effect: Effect):
        ''' Takes an Effect and adds it to the list of effects
            Can be RepeatEffect
            - RepeatEffect
            - RepeatCallbacksEffect

            * Not bueno, Drags performance
        '''
        # validate effect
        self.effects.append(effect)

    @override
    def onMount(self):
        return super().onMount()

    @override
    def dispose(self): 
        '''
        The method is called to delete the object
        '''
        # delete the effects
        self.effects.clear()

        # delete drawing
        del self.drawing

        # destroy the object's panel
        self.destroyWindow()

        self.isGarbage = True

    @override
    def update(self, dt: float, game: EngineInterface):
        '''
        The method is called every frame to update the object
        '''
        self._update_pos_flags(game)

        super().update(dt, self.drawing)

    def _update_pos_flags(self, game: EngineInterface):
        # init all position flags to False
        self.past_left_extreme = False
        self.past_right_extreme = False
        self.above_roof = False
        self.below_floor = False
        self.on_floor = False
        self.on_roof = False
        self.in_view = False

        # update the position flags
        # check against horizontal extremes of the game_window
        if self.position.x <= 0:
            self.past_left_extreme = True
        elif self.bounds.x_end >= game.window_width - 1:
            self.past_right_extreme = True

        # check against vertical extremes
        if self.bounds.y_end == game.floor:
            self.on_floor = True
        elif self.bounds.y_end > game.floor:
            self.below_floor = True
        elif self.bounds.y_start == game.roof:
            self.above_roof = True
        elif self.position.y < game.roof:
            self.on_roof = True

        # check if the object is in view
        if (not self.past_left_extreme and not self.past_right_extreme) and (not self.above_roof and not self.below_floor):
            self.in_view = True

    def _check_for_new_config(self) -> bool:
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
        return True if self._check_for_new_config() else self.shouldRedraw()
           
    @override
    def render(self, game: EngineInterface):
        ''' 
        Renders the object to the screen 
        - It is called after the update object is called
        - It first reconfigures the panel_window if the metrics have changed
        - Then, It calls the panel's redraw method
        '''   
        print(f'----Trying to render')
        # handle reconfiguring
        # handle repositiong and resizing of the panel_window
        if (self._check_for_new_config()): self._reconfigurePanelWindow(game)

        # redraw the window if the panel_window needs to redraw
        # and the game is not in debug mode
        # do not attempt redraw if panel does not exist
        print(f'--- SHOULDREDRAW {self.shouldRedraw()}')
        print(f'--- PANEL WINDOW EXISTS {self.panel_window_exists()}')

        if (self.shouldRedraw() and not game.debug_mode) and self.panel_window_exists(): 
            self.redrawWindow()

        # declare garbage if object is non-persistent and is out of view
        if not self.isPersistent and not self.in_view: self.isGarbage = True
    
    def _reconfigurePanelWindow(self, game: EngineInterface) -> bool:
        ''' Handles the change in the metrics of the 
         - Repositiong and resizing the object's panel_window
         - Since repositioning and resizing the panel_window is weirdly non-functional in curses,
         this function is a workaround to rebuild the panel_window in the new position and size.
         The approach works but it is very costly.
        '''
        
        # the object's panel should be rendered in a fresh configs
        # pop the old panel_window if it exists
        if self.panel_window_exists() and not game.debug_mode: self.destroyWindow()

        # create a new panel_window with the new configs
        # if the object is in view
        if self.in_view and not game.debug_mode: self.createPanelWindow(self.size, self.pos)

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

    
''''
Object that can collide with other objects that have a collider.
'''
class CollidableObject (Object, Collider):
    def __init__(
                 self, 
                 
                 tag: str = "", 
                 drawing: DrawingInterface = None, 
                 position: Vec2 = Vec2(0, 0), 
                 priority: int =0, 
                 colliderFill: ColliderFill = ColliderFill.FILLED,
                 ):
        
        Object.__init__(self, drawing, tag, position, priority)
        Collider.__init__(self, colliderFill)

    def update(self, dt: float):
        super().update(dt, self.drawing)

    @override
    def dispose(self):
        self.clear_collisions()
        super().dispose()

    @override
    def collide_with(self, other: ObjectInterface, collisionType: CollisionType):
        ''' Takes another object and checks if they are colliding
        '''
        # if this is on top of the other object
        # this is on the floor
        if self.position.y + self.size.y  == other.position.y:
            self.on_floor = True

        return super().collide_with(other, collisionType)
