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

from g.one.menu_item import *


class Menu():
    def __init__(self, window=None):
        if window is not None:
            window.push_handlers(self)
            self.window = window
        self.batch = pyglet.graphics.Batch()
        self._selected = 0
        self.options = []

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.DOWN:
            self.selected = min(self.selected+1, len(self.options)-1)
        else:
            self.options[self.selected].on_key_release(symbol, modifiers)

    def draw(self):
        self.batch.draw()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self.options[self._selected].set_selected(False)
        self._selected = value
        self.options[self._selected].set_selected(True)

    def delete(self):
        self.window.remove_handlers(self)
        self.options = None


class MainMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          'G - One',
          font_name='Times New Roman',
          font_size=36,
          x=427, y=400,
          color=(255, 255, 0, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = [
          MenuAction(self, "New Game", self.new_game_pressed, 427, 160),
          MenuItem(self, "Load Game", 427, 130),
          MenuItem(self, "Highscore List", 427, 100),
          MenuItem(self, "Options", 427, 70),
          MenuAction(self, "Exit", quit, 427, 40)
        ]
        self.selected = 0

    def new_game_pressed(self):
        self.window.change_stage(NewGameMenu(self.window))


class NewGameMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          'New Game',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = [
          OptionSelector(self, "Play as", ["Earthlings", "Aliens"], 150, 160),
          OptionSelector(self, "Difficulty", ["Normal", "Hard"], 150, 130),
          OptionSelector(self, "Number of Players", ["One", "Two"], 150, 100),
          HorizontalSelection([
            MenuAction(self, "Back", self.back_pressed, 100, 40),
            MenuAction(self, "Start", self.start_pressed, 754, 40)
          ])
        ]
        self.selected = 0

    def back_pressed(self):
        self.window.change_stage(MainMenu(self.window))

    def start_pressed(self):
        from g.one.game import Game
        earth = self.options[0].selected == 0
        difficulty = self.options[1].selected
        players = self.options[2].selected + 1
        game = Game(self.window, earth, difficulty, players)
        self.window.change_stage(game)
