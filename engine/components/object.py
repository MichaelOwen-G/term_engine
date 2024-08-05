from enum import Enum
from typing import List, override

from engine.components.drawing import Drawing

from ._interfaces import ColliderInterface, ObjectInterface, DrawingInterface

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
    def __init__(self, tags: list[str] = [], drawing: DrawingInterface = None, position: Vec2 = Vec2(0, 0), priority: int =0, isPersistent = False):
        ObjectInterface.__init__(self, drawing, tags, isPersistent=isPersistent)

        super().__init__(drawing.maxSize, position, priority = priority)

        # To keep track of the metrics
        self._back_position: Vec2 = None
        self._back_size :Vec2 = None
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
    def onMount(self, game = None, screen = None):
        return super().onMount(game=game, screen=screen)

    @override
    def dispose(self): 
        '''
        The method is called to delete the object
        '''
        # delete the effects
        self.effects.clear()

        # destroy the object's panel
        self.destroyWindow()

        self.isGarbage = True

    @override
    def update(self, dt: float = 0, game = None):
        '''
        The method is called every frame to update the object
        '''
        # delay update until it is deleted if this is garbage
        if self.isGarbage: return

        self._update_pos_flags(game)

        super().update(dt, self.drawing)

    def _update_pos_flags(self, game):
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
        if self.bounds.y_end == game.floor: self.on_floor = True

        elif self.bounds.y_end > game.floor: self.below_floor = True
        
        elif self.bounds.y_start == game.roof:  self.on_roof = True

        elif self.bounds.y_start < game.roof: self.above_roof = True

        # check if the object is in view
        if (not self.past_left_extreme and not self.past_right_extreme) and (not self.above_roof and not self.below_floor):
            self.in_view = True

    @override    
    def shouldRedraw(self) -> bool:
        if self._check_for_new_config(): return True
        return super().shouldRedraw()

    def _check_for_new_config(self) -> bool:
        ''' Checks if the object's metrics have changed since the last time it was rendered'''
        
        print(f'BACK POS: {self._back_position}')

        # if back configd are empty, then the object has never been rendered before
        if (self._back_position is None or self._back_size is None): return True

        if ((not self._back_position == self.position) or (not self._back_size == self.size)):
            return True

        return False
           
    @override
    def render(self, game):
        ''' 
        Renders the object to the screen 
        - It is called after the update object is called
        - It first reconfigures the panel_window if the metrics have changed
        - Then, It calls the panel's redraw method
        '''   
        print(f'----Re rendering')

        if self.isGarbage: return


        # handle reconfiguring
        # handle repositiong and resizing of the panel_window
        if (self._check_for_new_config()): self._reconfigurePanelWindow(game)

        # redraw the window if the panel_window needs to redraw
        # and the game is not in debug mode
        # print(f'--- PANEL SHOULDREDRAW {super().shouldRedraw()}')

        if (super().shouldRedraw()): self.redrawWindow()


    def _reconfigurePanelWindow(self, game) -> bool:
        ''' Handles the change in the metrics of the 
         - Repositiong and resizing the object's panel_window
         - Since repositioning and resizing the panel_window is weirdly non-functional in curses,
         this function is a workaround to rebuild the panel_window in the new position and size.
         The approach works but it is very costly.
        '''
    
        
        # if object is being rendered for the first time,
        # i.e _back_position and _back_size are zero
        if self._back_position is None or self._back_position is None:
            # create panel window
            # only if the object is in view
            if not game.debug_mode and self.in_view: self.createPanelWindow(self.size, self.pos)

            self._back_position = Vec2().replace_with(self.pos)
            self._back_size = Vec2().replace_with(self.size)

        else:
            # if the position has changed
            # - reposition the panel_window
            if not self._back_position == self.pos:
                self.destroyWindow()
                if not game.debug_mode and self.in_view: self.reposition_window()
                self._back_position.replace_with(self.pos)

            # if the size has changed
            if not self._back_size == self.size:
                self.destroyWindow()
                if not game.debug_mode and self.in_view: self.panelWindow.resize(self.size.y, self.size.x)
                
                # update the back_size
                self._back_size.replace_with(self.size)

        # update bounds
        self.bounds.pos = self.pos
        self.bounds.size = self.size

        # declare garbage if object is non-persistent and is out of view
        if not self.isPersistent and not self.in_view: self.isGarbage = True


''' 
            OBJECT WITH COLLISION MADE POSSIBLE 
            
 - Has a collider that takes collisions off other colliders 
 
'''
class ColliderFill(Enum):
    FILLED = 1
    HOLLOW = 2
    
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

class Collider(ColliderInterface):
    def __init__(self, colliderFill: ColliderFill):
        
        # a list of the objects the collier has collided with
        self._collisions: List[CollisionData] = []

        super().__init__(colliderFill)

    def collide_with(self, other: ObjectInterface, collisionType: 'CollisionType'):
        self._collisions.append(CollisionData(other, collisionType))

    
''''
Object that can collide with other objects that have a collider.
'''
class CollidableObject (Object, Collider):
    def __init__(
                 self, 
                 
                 tags: list[str] = [], 
                 drawing: DrawingInterface = None, 
                 position: Vec2 = Vec2(0, 0), 
                 priority: int =0, 
                 colliderFill: ColliderFill = ColliderFill.FILLED,
                 isPersistent = False
                 ):
        
        Object.__init__(self, tags = tags,  drawing = drawing, position=position, priority=priority, isPersistent = isPersistent)
        Collider.__init__(self, colliderFill)

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



''' 
                            TEXT OBJECT 

'''

class TextBox(Object):
    '''
    Has only one item in self.drawing.state
    '''
    def __init__(self, text:str, tags = [], x = 0, y = 0, priority= 0):
        drawing = Drawing(tag=text, drawingStates=[text])

        super().__init__(tags=tags, drawing=drawing, position=Vec2(x, y), priority=priority)

    @property
    def text(self) -> str:
        return self.drawing.states[0]
    
    @text.setter
    def text(self, new_text: str):
        self.drawing.states[0] = new_text