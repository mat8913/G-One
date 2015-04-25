from g.one.resources import Resources
import g.one.ship
import pyglet
from pyglet.window import key
from g.one.state import State
from g.one.menu import MainMenu

class GameWindow(pyglet.window.Window):
    state = State.MENU
    players = 0
    paused = False

    def __init__(self):
        pyglet.window.Window.__init__(self,width=854,height=480,resizable=True)
        self.register_event_type('player1')
        self.register_event_type('player2')
        self.register_event_type('menu_key')
        self.menu = MainMenu(self)

    def on_draw(self):
        self.clear()
        Resources.batch.draw()
        if self.state == State.MENU:
            self.menu.draw()

    def on_key_press(self, symbol, modifiers):
        if self.state == State.GAME:
            if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
                self.dispatch_event('player1', symbol, True)
            elif symbol == key.ESCAPE:
                self.paused = not self.paused

    def on_key_release(self, symbol, modifiers):
        if self.state == State.MENU:
            self.dispatch_event('menu_key', symbol)
        elif self.state == State.GAME:
            if symbol in [key.LEFT,key.RIGHT,key.UP,key.DOWN]:
                self.dispatch_event('player1', symbol, False)

    def change_state(self, state):
        if (self.state,state) == (State.MENU,State.GAME):
            del self.menu
            self.ship1_sprite = g.one.ship.Ship(self,1)
            if self.players == 2:
                self.ship2_sprite = g.one.ship.Ship(self,2)
        self.state = state

    def on_resize(self, width, height):
        adjwidth = (height * 16) // 9
        adjheight = (width * 9) // 16
        if adjwidth < width:
            pyglet.gl.glViewport((width-adjwidth)//2, 0, adjwidth, height)
        else:
            pyglet.gl.glViewport(0, (height-adjheight)//2, width, adjheight)

        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, 854, 0, 480, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

def main():
    Resources.init()
    window = GameWindow()
    pyglet.app.run()
