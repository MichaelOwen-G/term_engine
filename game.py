
from bird_drawing import bird
from engine.core import Game
from pipe_drawing import spawn_bottom_pipes, spawn_top_pipes


game = Game(50, 25)

game.addObject(bird)

game.addEffect(spawn_bottom_pipes)
# game.addEffect(spawn_top_pipes)

game.run()