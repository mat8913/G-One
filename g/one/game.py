import pyglet
from pyglet.window import key

from g.one.ship import Ship
from g.one.resources import Resources
from g.one.options import Options

class Game(pyglet.event.EventDispatcher):
    def __init__(self, window, players=1):
        window.push_handlers(self)
        self.batch = pyglet.graphics.Batch()
        self.register_event_type('player1')
        self.register_event_type('player2')
        self.players = players
        self.paused = False
        self.register_event_type('player1')
        self.ship1_sprite = Ship(self, 1)
        if self.players == 2:
            self.register_event_type('player2')
            self.ship2_sprite = Ship(self, 2)

    def draw(self):
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.paused = not self.paused
            return
        for k, v in Options.options['controls'][0].items():
            if symbol == v:
                self.dispatch_event('player1', k, True)
                return

    def on_key_release(self, symbol, modifiers):
        for k, v in Options.options['controls'][0].items():
            if symbol == v:
                self.dispatch_event('player1', k, False)
                return
