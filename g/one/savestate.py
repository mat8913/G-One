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

from pyglet.resource import get_settings_path

from g.one.game_pickler import GamePickler, GameUnpickler


def get_filename(statenum):
    return get_settings_path("g-one") + "/save_" + str(statenum) + ".p"


def get_state_info(statenum):
    filename = get_filename(statenum)
    try:
        with open(filename, 'rb') as f:
            return GameUnpickler(f, None).load()
    except Exception:
        return None


def save_state(statenum, game):
    filename = get_filename(statenum)
    with open(filename, 'wb') as f:
        pickler = GamePickler(f)
        game_info = str(len(game.players))
        game_info += " player, "
        game_info += "Earthlings, " if game.earth else "Aliens, "
        game_info += "Level " + str(game.level) + ", "
        game_info += ["Normal", "Hard"][game.difficulty]
        pickler.dump(game_info)
        pickler.dump(game)


def load_state(statenum, window):
    filename = get_filename(statenum)
    with open(filename, 'rb') as f:
        pickler = GameUnpickler(f, window)
        pickler.load()
        return pickler.load()
