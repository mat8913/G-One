from g.one.resources import Resources
import g.one.ship
import pyglet
from pyglet.window import key

class GameWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self)
        self.register_event_type('player1')

    def on_draw(self):
        self.clear()
        Resources.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
            self.dispatch_event('player1', symbol, True)

    def on_key_release(self, symbol, modifiers):
        if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
            self.dispatch_event('player1', symbol, False)

def main():
    Resources.init()
    window = GameWindow()
    mysprite = g.one.ship.Ship(window)
    pyglet.app.run()
