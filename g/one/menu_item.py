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


class MenuItem():
    def __init__(self, menu, text, x=0, y=0, center=True):
        self.menu = menu
        self.label = pyglet.text.Label(
          text,
          font_name='Times New Roman',
          font_size=16,
          x=x, y=y,
          anchor_x='center', anchor_y='center',
          batch=menu.batch
        )
        if not center:
            self.label.anchor_x = 'left'

    def on_key_release(self, symbol, modifiers):
        pass

    def set_selected(self, selected):
        if selected:
            self.label.color = (255, 255, 0, 255)
        else:
            self.label.color = (255, 255, 255, 255)

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, value):
        self.label.text = value


class MenuAction(MenuItem):
    def __init__(self, menu, text, action, x=0, y=0):
        MenuItem.__init__(self, menu, text, x, y)
        self.action = action

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.action()


class KeySelector(MenuItem):
    def __init__(self, menu, key, x=0, y=0):
        MenuItem.__init__(self, menu, "", x, y)
        self.selected_key = key

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ENTER:
            self.menu.window.push_handlers(on_key_release=self.select_key)

    def select_key(self, symbol, modifiers):
        self.selected_key = symbol
        self.menu.window.remove_handlers(on_key_release=self.select_key)
        return True

    @property
    def selected_key(self):
        return self._selected_key

    @selected_key.setter
    def selected_key(self, value):
        self._selected_key = value
        self.label.text = key.symbol_string(value)


class OptionSelector(MenuItem):
    def __init__(self, menu, text, options, x, y):
        MenuItem.__init__(self, menu, text, x, y, center=False)
        self.option_label = pyglet.text.Label(
          "<< >>",
          font_name='Times New Roman',
          font_size=16,
          x=854-x, y=y,
          anchor_x='right', anchor_y='center',
          batch=menu.batch
        )
        self.options = options
        self.selected = 0

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.RIGHT:
            self.selected = min(self.selected+1, len(self.options)-1)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.option_label.text = "<< " + self.options[value] + " >>"


class Slider(MenuItem):
    def __init__(self, menu, text, x, y):
        MenuItem.__init__(self, menu, text, x, y, center=False)
        self.width = 124

        # Co-ordinates for the slider itself (not the text)
        self.y = y
        self.left = 730-x
        self.right = self.left + self.width

        self.background = self.menu.batch.add(
                4, pyglet.gl.GL_TRIANGLE_STRIP, pyglet.graphics.Group(),
                ('v2i', (self.left, y-2,
                         self.left, y+2,
                         self.right, y-2,
                         self.right, y+2)),
                ('c3B', (255, 255, 255,
                         255, 255, 255,
                         255, 255, 255,
                         255, 255, 255))
            )
        self.slider = self.menu.batch.add(
                3, pyglet.gl.GL_TRIANGLES, pyglet.graphics.Group(),
                ('v2i', (0, y-10, 0, y-10, 0, y+10)),
                ('c3B', (255, 255, 255, 255, 255, 255, 255, 255, 255,))
            )
        self.value = 100

    def on_text_motion(self, motion):
        if motion == key.MOTION_LEFT:
            self.value = max(self.value-1, 0)
        elif motion == key.MOTION_RIGHT:
            self.value = min(self.value+1, 100)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        center = self.left + (self.width * value)//100
        self.slider.vertices[0] = center - 5
        self.slider.vertices[2] = center + 5
        self.slider.vertices[4] = center

    def __del__(self):
        # Free vertex lists from memory.
        self.background.delete()
        self.slider.delete()


class HorizontalSelection():
    def __init__(self, options):
        self.options = options
        self._selected = 0

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.RIGHT:
            self.selected = min(self.selected+1, len(self.options)-1)
        else:
            self.options[self.selected].on_key_release(symbol, modifiers)

    def set_selected(self, selected):
        self.options[self.selected].set_selected(selected)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self.options[self._selected].set_selected(False)
        self._selected = value
        self.options[self._selected].set_selected(True)
