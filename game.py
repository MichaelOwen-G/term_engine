from engine.core import Game

from bird import Bird
from engine.metrics.duration import Duration, DurationMetrics
from pipe import TopPipe
from pipe_spawner import PipeSpawner


game = Game(70, 35, debug_mode=False)

bird = Bird(x = 2, y = 2)

game.addObject(bird)

pipe_spawner = PipeSpawner(Duration(DurationMetrics.SECONDS, 3))

# game.addEffect(pipe_spawner)

top_pipe = TopPipe(10, 
                    x = 30, 
                    y = 10,
                    )
game.addObject(top_pipe)
game.run()