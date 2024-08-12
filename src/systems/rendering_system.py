from ._interfaces import ObjectSystem
from ..panel._interfaces import PanelInterface


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
    