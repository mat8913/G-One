from g.one.resources import Resources
import g.one.ship
import pyglet
from pyglet.window import key

class GameWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self,width=854,height=480,resizable=True)
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
    mysprite = g.one.ship.Ship(window)
    pyglet.app.run()
