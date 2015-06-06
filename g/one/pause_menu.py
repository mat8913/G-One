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

from g.one.menu import Menu
from g.one.menu_item import *


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self)
        self.game = game
        self.title = pyglet.text.Label(
          'Paused',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = [
          MenuAction(self, "Resume", self.resume_pressed, 427, 160),
          MenuItem(self, "Save Game", 427, 130),
          MenuItem(self, "Highscore List", 427, 100),
          MenuAction(self, "Exit", self.exit_pressed, 427, 70),
        ]
        self.selected = 0

    def resume_pressed(self):
        self.game.change_pause(None)

    def exit_pressed(self):
        self.game.exit()
