
from ..components._interfaces import ObjectInterface
from ._interfaces import ObjectSystem
from ..panel._interfaces import PanelInterface


class RenderingSystem(ObjectSystem):
    '''
        Responsible for rendering the Object's panels on the screen
    '''

    def __init__(self, game_engine):
        super().__init__(game_engine)

    def run_all(self):
        game_objs = self.game_engine.objects

        for obj in game_objs:
            self.run(obj)

    def run(self, object: PanelInterface):
        '''
        Rerenders/Redraws the front buffer of an object's panel to the screen
        '''
        
        # validate args
        if not isinstance(object, ObjectInterface):
            raise TypeError(" object {0} is not of type ObjectType".format(object))

        
        # redraw/rerender the object's panels if the object wants to redraw and 
        # the object is in view
        if object.shouldRedraw(): object.render(self.game_engine)
