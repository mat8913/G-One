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

import string
from sys import exit as quit
from itertools import zip_longest

import pyglet
from pyglet.window import key

from g.one import savestate
from g.one import highscores
from g.one.menu_item import *
from g.one.resources import Resources
from g.one.background_music import BackgroundMusic
from g.one.options import Options


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
        the overriding method.  AFTER appending menu items to self.items, the
        overriding method should initialise self.selected.

        self.batch is set up as a drawing batch which all menu items should be
        added to.
        """
        if window is not None:
            window.push_handlers(self)
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self._selected = 0
        self.deleted = False
        self.items = []

    def on_key_release(self, symbol, modifiers):
        """Called when a key is released.

        If the up or down arrow keys were released, select the next or previous
        item of the menu respectively.  Otherwise, the keyrelease is send to
        the currently selected menu item.
        """
        if symbol == key.UP:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.DOWN:
            self.selected = min(self.selected+1, len(self.items)-1)
        else:
            self.items[self.selected].on_key_release(symbol, modifiers)

    def draw(self):
        """Draws the menu."""
        self.batch.draw()

    def delete(self):
        """Call this when the menu is to be deleted."""
        if self.window is not None:
            self.window.remove_handlers(self)
        self.items = None  # Break the circular references.
        self.deleted = True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        """Informs menu items when they are (de)selected."""
        self.items[self._selected].set_selected(False)
        self._selected = value
        self.items[self._selected].set_selected(True)


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
        self.items = [
          MenuAction(self, "New Game", self.new_game_pressed, 427, 160),
          MenuAction(self, "Load Game", self.load_game_pressed, 427, 130),
          MenuAction(self, "Highscore List", self.highscore_list_pressed,
                     427, 100),
          MenuAction(self, "Options", self.options_pressed, 427, 70),
          MenuAction(self, "Exit", quit, 427, 40)
        ]
        self.selected = 0
        BackgroundMusic.play(Resources.menu_music)

    def new_game_pressed(self):
        self.window.change_stage(NewGameMenu(self.window))

    def load_game_pressed(self):
        self.window.change_stage(LoadGameMenu(self.window))

    def highscore_list_pressed(self):
        self.window.change_stage(HighscoresMenu(self.window))

    def options_pressed(self):
        self.window.change_stage(OptionsMenu(self.window))


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
        self.items = [
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
        earth = self.items[0].selected == 0
        difficulty = self.items[1].selected
        players = self.items[2].selected + 1
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
        self.items = []
        self.items += [self.savestate_option(i) for i in range(3)]
        self.items += [MenuAction(self, "Back", self.back_pressed, 100, 40)]
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


class HighscoresMenu(Menu):
    def __init__(self, window, earth=True):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          '',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.items = [
          HorizontalSelection([
            MenuAction(self, "Back", self.back_pressed, 100, 40),
            MenuAction(self, "Earthlings", self.earth_pressed, 600, 40),
            MenuAction(self, "Aliens", self.aliens_pressed, 754, 40)
          ])
        ]
        self.headings = [
          pyglet.text.Label(
            'Rank',
            font_name='Times New Roman',
            font_size=16,
            x=100, y=350,
            color=(255, 255, 255, 255),
            anchor_x='left', anchor_y='center',
            batch=self.batch),
          pyglet.text.Label(
            'Name',
            font_name='Times New Roman',
            font_size=16,
            x=200, y=350,
            color=(255, 255, 255, 255),
            anchor_x='left', anchor_y='center',
            batch=self.batch),
          pyglet.text.Label(
            'Difficulty',
            font_name='Times New Roman',
            font_size=16,
            x=580, y=350,
            color=(255, 255, 255, 255),
            anchor_x='left', anchor_y='center',
            batch=self.batch),
          pyglet.text.Label(
            'Score',
            font_name='Times New Roman',
            font_size=16,
            x=700, y=350,
            color=(255, 255, 255, 255),
            anchor_x='left', anchor_y='center',
            batch=self.batch),
        ]

        self.scores = [
          [
            pyglet.text.Label(
              str(i+1) + '.',
              font_name='Times New Roman',
              font_size=16,
              x=100, y=320 - 20*i,
              color=(255, 255, 255, 255),
              anchor_x='left', anchor_y='center',
              batch=self.batch),
            pyglet.text.Label(
              '',
              font_name='Times New Roman',
              font_size=16,
              x=200, y=320 - 20*i,
              color=(255, 255, 255, 255),
              anchor_x='left', anchor_y='center',
              batch=self.batch),
            pyglet.text.Label(
              '',
              font_name='Times New Roman',
              font_size=16,
              x=580, y=320 - 20*i,
              color=(255, 255, 255, 255),
              anchor_x='left', anchor_y='center',
              batch=self.batch),
            pyglet.text.Label(
              '',
              font_name='Times New Roman',
              font_size=16,
              x=700, y=320 - 20*i,
              color=(255, 255, 255, 255),
              anchor_x='left', anchor_y='center',
              batch=self.batch),
          ] for i in range(10)]
        self.selected = 0
        self.earth = earth

    @property
    def earth(self):
        return self._earth

    @earth.setter
    def earth(self, value):
        self._earth = value
        self.title.text = "Highscores - " + (
          "Earthlings" if value else "Aliens")
        score_list = highscores.load_highscores()[0 if value else 1]
        for row, data in zip_longest(self.scores, score_list):
            if data is None:
                row[1].text = "..."
                row[2].text = ""
                row[3].text = ""
            else:
                row[1].text = data[0]
                row[2].text = ["Normal", "Hard"][data[1]]
                row[3].text = str(data[2])

    def earth_pressed(self):
        self.earth = True

    def aliens_pressed(self):
        self.earth = False

    def back_pressed(self):
        self.window.change_stage(MainMenu(self.window))


class OptionsMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          'Options',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.items = [
          OptionSelector(self, "Fullscreen:", ["Off", "On"], 150, 160),
          Slider(self, "Music:", 150, 130),
          Slider(self, "Sound effects:", 150, 100),
          MenuItem(self, "Controls", 150, 70, center=False),
          MenuAction(self, "Back", self.back_pressed, 100, 40)
        ]
        if Options.options['fullscreen']:
            self.items[0].selected = 1
        else:
            self.items[0].selected = 0
        self.items[1].value = Options.options['music']
        self.items[2].value = Options.options['sound effects']
        self.selected = 0

    def on_key_release(self, symbol, modifiers):
        Menu.on_key_release(self, symbol, modifiers)
        if self.deleted:
            return
        Options.options['fullscreen'] = self.items[0].selected == 1
        Options.changed()

    def on_text_motion(self, motion):
        if isinstance(self.items[self.selected], Slider):
            self.items[self.selected].on_text_motion(motion)
        Options.options['music'] = self.items[1].value
        Options.options['sound effects'] = self.items[2].value
        Options.changed()

    def back_pressed(self):
        Options.save()
        self.window.change_stage(MainMenu(self.window))


class GameOverMenu(Menu):
    def __init__(self, window, score, difficulty, earth):
        Menu.__init__(self, window)
        self.score = score
        self.difficulty = difficulty
        self.earth = earth
        self.highscore = highscores.is_highscore(earth, score)
        self.title = pyglet.text.Label(
          'Game Over',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.score_label = pyglet.text.Label(
          'Score: ' + str(score),
          font_name='Times New Roman',
          font_size=16,
          x=427, y=350,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.difficulty_label = pyglet.text.Label(
          'Difficulty: ' + ["Normal", "Hard"][difficulty],
          font_name='Times New Roman',
          font_size=16,
          x=427, y=320,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.earh_label = pyglet.text.Label(
          'Playing as: ' + "Earthlings" if earth else "Aliens",
          font_name='Times New Roman',
          font_size=16,
          x=427, y=290,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        if self.highscore:
            self.enter_name_label = pyglet.text.Label(
              'Please enter your name and press enter to continue:',
              font_name='Times New Roman',
              font_size=16,
              x=427, y=200,
              color=(255, 255, 255, 255),
              anchor_x='center', anchor_y='center',
              batch=self.batch
            )
            self.player_name_label = pyglet.text.Label(
              '',
              font_name='Times New Roman',
              font_size=16,
              x=427, y=170,
              color=(255, 255, 255, 255),
              anchor_x='center', anchor_y='center',
              batch=self.batch
            )
            self.player_name = ""
        else:
            self.enter_name_label = pyglet.text.Label(
              'You did not achieve a high score, press enter to continue.',
              font_name='Times New Roman',
              font_size=16,
              x=427, y=200,
              color=(255, 255, 255, 255),
              anchor_x='center', anchor_y='center',
              batch=self.batch
            )

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ENTER:
            if self.highscore:
                highscores.add_highscore(self.earth, self.player_name,
                                         self.difficulty, self.score)
            self.window.change_stage(HighscoresMenu(self.window, self.earth))

    def on_text(self, text):
        if not self.highscore:
            return
        if text not in string.whitespace or text == ' ':
            self.player_name += text

    def on_text_motion(self, motion):
        if not self.highscore:
            return
        if motion == key.MOTION_BACKSPACE:
            self.player_name = self.player_name[:-1]

    @property
    def player_name(self):
        return self._player_name

    @player_name.setter
    def player_name(self, value):
        self._player_name = value
        self.player_name_label.text = value
