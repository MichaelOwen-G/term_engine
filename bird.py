
import time
from typing import override
from engine.components.drawing import Drawing, DrawingStack
from engine.components.object import CollidableObject, CollisionType, Object
from engine.effects.repeat_effect import RepeatCallbacksEffect, RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2

import example_package_gachanja_project
class Bird(CollidableObject):
    def __init__(self, x = 0, y = 0, tags: list[str] = [], priority = 0):
       
        birdDrawing = self.draw_bird()

        self.dead = False

        self.key_presses =[]

        self.points = 0
        
        self.flap_sound = None
        self.hit_sound = None

        super().__init__(tags=tags, drawing=birdDrawing, position=Vec2(x, y), priority=priority, isPersistent = True)


    def draw_bird(self) -> Drawing:

        ''' The body of the bird '''
        wings = Drawing(tag = "wings", drawingStates= ['/\ .',  '__ .'])
        body = Drawing(tag = "body", drawingStates=   ['    >'])

         # create the bird drawing
        birdDrawing: DrawingStack = DrawingStack()

        ''' stack the two drawings together '''
        birdDrawing.add(wings.copy())
        birdDrawing.add(body.copy())

        return birdDrawing


    @override
    def onMount(self, **kwargs):
        
        game = kwargs.get('game', None)
        
        # load sound
        self.flap_sound = game.load_sound('flap.mp3')
        self.hit_sound = game.load_sound('hit.mp3')
        
        ''' ANIMATIONS '''
        # add the fly animation effect
        # define effect
        self.fly_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 550),
            )
        self.fly_effect.addCallback(self.fly_anim)
        
        self.addEffect(self.fly_effect)

        self.gravity_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 350),
            )

        self.gravity_effect.addCallback(self.gravitize)
        
        self.addEffect(self.gravity_effect)

        # define effect

        ''' ANIMATIONS '''
        return super().onMount()
    
    def gravitize(self, **kwargs):
        if not self.on_floor: self.position.y += 1

    
    def move_pipe(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.x += 1
    
    # fly animation
    def fly_anim(self, **kwargs):
        obj: Object = kwargs.get('object', None)

        obj.drawing.next_state()
        
    @override
    def update(self, **kwargs):
        dt   = kwargs.get('dt', 0)
        game = kwargs.get('game', None)
        
        key = game.stdscr.getch()
        
        if key == ord(' '): self.fly()

        super().update(dt, game)
        
    def fly(self):
        self.pos.y -= 4
        self.flap_sound.play()

    @override
    def listen_for_key_press(self) -> bool: 
        return True

    @override
    def collide_with(self, other, collisionType: CollisionType):
        
        self.hit_sound.play()
        self.dead = True
        
        super().collide_with(other, collisionType)
        
        time.sleep(1)

