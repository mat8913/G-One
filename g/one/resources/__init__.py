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
from pyglet.image.codecs.png import PNGImageDecoder


class Resources():
    @staticmethod
    def init():
        pyglet.resource.path = ['@g.one.resources']
        pyglet.resource.reindex()
        Resources.ship_image = Resources.load_image("ship.png")
        Resources.earth_bullet_image = Resources.load_image("earth_bullet.png")
        Resources.alien_bullet_image = Resources.load_image("alien_bullet.png")

    @staticmethod
    def load_image(filename):
        with pyglet.resource.file(filename) as f:
            decoder = PNGImageDecoder()
            return pyglet.image.load(filename, file=f, decoder=decoder)
