import pyglet
from pyglet.window import key

from g.one.ship import Ship
from g.one.resources import Resources

class Game(pyglet.event.EventDispatcher):
    def __init__(self, window, players=1):
        window.push_handlers(self)
        self.register_event_type('player1')
        self.register_event_type('player2')
        self.players = players
        self.paused = False
        self.register_event_type('player1')
        self.ship1_sprite = Ship(self,1)
        if self.players == 2:
            self.register_event_type('player2')
            self.ship2_sprite = Ship(self,2)

    def draw(self):
        Resources.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
            self.dispatch_event('player1', symbol, True)
        elif symbol == key.ESCAPE:
            self.paused = not self.paused

    def on_key_release(self, symbol, modifiers):
        if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
            self.dispatch_event('player1', symbol, False)
