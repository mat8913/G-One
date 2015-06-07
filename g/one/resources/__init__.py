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
    @classmethod
    def init(cls):
        pyglet.resource.path = ['@g.one.resources']
        pyglet.resource.reindex()
        cls.ship_image = cls.load_image("ship.png")
        cls.earth_bullet_image = cls.load_image("earth_bullet.png")
        cls.alien_bullet_image = cls.load_image("alien_bullet.png")
        cls.earth_player_image = cls.load_image("earth_player.png")
        cls.alien_player_image = cls.load_image("alien_player.png")
        cls.menu_music = MediaLoader("menu.wav")

    @staticmethod
    def load_image(filename):
        with pyglet.resource.file(filename) as f:
            decoder = PNGImageDecoder()
            return pyglet.image.load(filename, file=f, decoder=decoder)


class MediaLoader():
    def __init__(self, filename):
        self.filename = filename

    def __call__(self):
        return pyglet.resource.media(self.filename)
