# This file is part of G-One.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pyglet
from pyglet.window import key

from g.one.resources import Resources
from g.one.menu import MainMenu


class GameWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width=854, height=480,
                                      caption="G - One", resizable=True)
        self.current_stage = MainMenu(self)

    def on_draw(self):
        self.clear()
        self.current_stage.draw()

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        if symbol == key.F:
            self.set_fullscreen(not self.fullscreen)

    def change_stage(self, newstage):
        self.current_stage.delete()
        self.current_stage = newstage

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
