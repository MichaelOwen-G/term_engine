
from ..panel._interfaces import PanelInterface
from ..systems._interfaces import ObjectSystem

class TypingSystem(ObjectSystem):

    def __init__(self, game_engine):
        # define key that ends game window
        self.killer_key = ord('q')

        # game_engine.stdscr.keypad(True)

        super().__init__(game_engine)

    def run(self, dt: float, object: PanelInterface):
        if object.panelWindow == None: return None

        # get keystroke of the object panel
        key_pressed: int = object.panelWindow.getch()

        # print('KEY PRESSED')

        # print(object.key_pressed)

        # update the objects key_pressed
        object.key_pressed = key_pressed
        

