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

from g.one.resources import Resources
from g.one.game_window import GameWindow
from g.one.options import Options
from g.one.background_music import BackgroundMusic


def main():
    pyglet.options['audio'] = tuple(x
                                    for x in pyglet.options['audio']
                                    if x != 'pulse')
    Resources.init()
    BackgroundMusic.init()
    Options.load()
    window = GameWindow()
    pyglet.app.run()
