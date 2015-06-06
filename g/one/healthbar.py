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


class Healthbar():
    """The Healthbar class keeps track of a sprite's health and displays that
    information to the screen visually in the form of a bar.
    """
    def __init__(self, sprite, x=0, y=0):
        """Keyword arguments:

        sprite -- the sprite whose health will be displayed by this healthbar
        x, y   -- the coordinates to the bottom right of this healthbar
        """
        self.vlist = pyglet.graphics.vertex_list(
                4,
                ('v2i', (x, 0, x, y, x+10, 0, x+10, y)),
                ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0))
            )
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self):
        """Draws the healthbar to screen."""
        self.set_health(self.sprite.health)
        # It's faster to draw two triangles than one rectangle.
        self.vlist.draw(pyglet.gl.GL_TRIANGLE_STRIP)

    def set_health(self, health):
        """Updates the size of the healthbar to match the provided health."""
        self.vlist.vertices[1] = self.y+health
        self.vlist.vertices[5] = self.y+health

    def __del__(self):
        # Free the vertex list from memory when this healthbar is deleted.
        self.vlist.delete()
