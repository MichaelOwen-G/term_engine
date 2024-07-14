
from ..components._interfaces import ObjectInterface
from ..systems._interfaces import ObjectSystem
from ..panel._interfaces import PanelInterface


class RenderingSystem(ObjectSystem):
    '''
        Responsible for rendering the Object's panels on the screen
    '''

    def __init__(self, game_engine):
        super().__init__(game_engine)

    def run(self, dt: float, object: ObjectInterface):
        # validate args
        if not isinstance(object, ObjectInterface):
            raise TypeError(" object {0} is not of type ObjectType".format(object))

        self.render_object(object)

    def render_object(self, object: ObjectInterface):
        ''''
        Rerenders/Redraws the front buffer of an object's panel to the screen
        '''
        # redraw/rerender the object's panels if the object wants to redraw and 
        # the object is in view
        if object.shouldRerender(): object.render()
