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

from sys import exit as quit

import pyglet
from pyglet.window import key

from g.one import savestate
from g.one.menu_item import *
from g.one.resources import Resources
from g.one.background_music import BackgroundMusic


class Menu():
    """This is the abstract menu class.

    It provides the basics of a menu.  The items in a Menu can be selected
    vertically, using the up and down arrow keys.  If horizontal selection is
    required, a HorizontalSelection can be used.

    Subclass this to create other menus.
    """
    def __init__(self, window=None):
        """Initialise the Menu.

        If window is provided, self.on_key_release will be set up as an event
        handler.  Otherwise, call the method manually when needed.

        Override this method when subclassing but call it at the BEGINNING of
        the overriding method.  AFTER appending menu items to self.options, the
        overriding method should initialise self.selected.

        self.batch is set up as a drawing batch which all menu items should be
        added to.
        """
        if window is not None:
            window.push_handlers(self)
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self._selected = 0
        self.options = []

    def on_key_release(self, symbol, modifiers):
        """Called when a key is released.

        If the up or down arrow keys were released, select the next or previous
        item of the menu respectively.  Otherwise, the keyrelease is send to
        the currently selected menu item.
        """
        if symbol == key.UP:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.DOWN:
            self.selected = min(self.selected+1, len(self.options)-1)
        else:
            self.options[self.selected].on_key_release(symbol, modifiers)

    def draw(self):
        """Draws the menu."""
        self.batch.draw()

    def delete(self):
        """Call this when the menu is to be deleted."""
        if self.window is not None:
            self.window.remove_handlers(self)
        self.options = None  # Break the circular references.

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        """Informs menu items when they are (de)selected."""
        self.options[self._selected].set_selected(False)
        self._selected = value
        self.options[self._selected].set_selected(True)


# The menus below follow the patterns described in the docstrings above and
# should be self-explanatory.

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
          MenuAction(self, "Load Game", self.load_game_pressed, 427, 130),
          MenuItem(self, "Highscore List", 427, 100),
          MenuItem(self, "Options", 427, 70),
          MenuAction(self, "Exit", quit, 427, 40)
        ]
        self.selected = 0
        BackgroundMusic.play(Resources.menu_music)

    def new_game_pressed(self):
        self.window.change_stage(NewGameMenu(self.window))

    def load_game_pressed(self):
        self.window.change_stage(LoadGameMenu(self.window))


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


class LoadGameMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          'Load Game',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = []
        self.options += [self.savestate_option(i) for i in range(3)]
        self.options += [MenuAction(self, "Back", self.back_pressed, 100, 40)]
        self.selected = 0

    def back_pressed(self):
        self.window.change_stage(MainMenu(self.window))

    def load_state_function(self, statenum):
        def load_state():
            game = savestate.load_state(statenum, self.window)
            self.window.change_stage(game)
        return load_state

    def savestate_option(self, statenum):
        y = 160 - 30*statenum
        statenum_text = "State " + str(statenum+1) + ": "
        info = savestate.get_state_info(statenum)
        if info is None:
            return MenuItem(self, statenum_text + "Empty", 427, y)
        else:
            return MenuAction(self,
                              statenum_text + info,
                              self.load_state_function(statenum),
                              427, y)
