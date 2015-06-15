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

filename = get_settings_path("g-one") + "/highscores.p"


def add_highscore(name, score):
    highscores = load_highscores()
    highscores.append((name, score))
    highscores.sort(key=lambda x: x[1], reverse=True)
    while len(highscores) > 10:
        del highscores[-1]
    save_highscores(highscores)
    return highscores


def is_highscore(score):
    highscores = load_highscores()
    if len(highscores) < 10:
        return True
    else:
        return score > highscores[-1][1]


def load_highscores():
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return []


def save_highscores(highscores):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        pickle.dump(highscores, f)
