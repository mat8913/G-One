import pyglet
from pyglet.window import key

from g.one.ship import Ship
from g.one.resources import Resources
from g.one.options import Options


class Game(pyglet.event.EventDispatcher):
    def __init__(self, window, play_as, difficulty, players=1):
        window.push_handlers(self)
        self.batch = pyglet.graphics.Batch()
        self.paused = False
        self.players = []
        for i in range(1, players+1):
            self.register_event_type('player' + str(i))
            self.players.append(Ship(self, i))

    def draw(self):
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.paused = not self.paused
            return
        for player in range(1, len(self.players)+1):
            for k, v in Options.options['controls'][player-1].items():
                if symbol == v:
                    self.dispatch_event('player' + str(player), k, True)
                    return

    def on_key_release(self, symbol, modifiers):
        for player in range(1, len(self.players)+1):
            for k, v in Options.options['controls'][player-1].items():
                if symbol == v:
                    self.dispatch_event('player' + str(player), k, False)
                    return
