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

import pickle
import os

from pyglet.resource import get_settings_path
from pyglet.window import key


class Options():
    filename = get_settings_path("g-one") + "/options.p"

    default_controls = [
      {
        key.UP:    key.UP,
        key.RIGHT: key.RIGHT,
        key.DOWN:  key.DOWN,
        key.LEFT:  key.LEFT,
        key.SPACE: key.SPACE
      },
      {
        key.UP:    key.W,
        key.RIGHT: key.D,
        key.DOWN:  key.S,
        key.LEFT:  key.A,
        key.SPACE: key.LSHIFT
      }
    ]

    default_options = {
      'fullscreen': False,
      'music': 100,
      'sound effects': 100,
      'controls': default_controls
    }

    @staticmethod
    def load():
        Options.options = Options.options_from_file(Options.filename)
        if Options.options is None:
            Options.options = Options.default_options

    @staticmethod
    def save():
        Options.options_to_file(Options.filename)

    @staticmethod
    def options_from_file(filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    @staticmethod
    def options_to_file(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            pickle.dump(Options.options, f)
