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

from pyglet.graphics import Batch


class GamePickler(pickle.Pickler):
    """Pickler class for Game. Ensures no attempt is made to pickle the drawing
    batch and window. Use GameUnpickler to unpickle.
    """
    def persistent_id(self, obj):
        from g.one.game_window import GameWindow
        if isinstance(obj, Batch):
            return "batch"
        elif isinstance(obj, GameWindow):
            return "window"
        else:
            return None


class GameUnpickler(pickle.Unpickler):
    """Unpickler class for Game. Provide a window to be passed to unpickled
    objects. The drawing batch will be created.
    """
    def __init__(self, file, window):
        super().__init__(file)
        self.batch = Batch()
        self.window = window

    def persistent_load(self, pid):
        if pid == "batch":
            return self.batch
        elif pid == "window":
            return self.window
        else:
            raise pickle.UnpicklingError("unsupported persistent object")
