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

from g.one.resources import Resources
from g.one.sprite import GameSprite
from g.one.bullet import Bullet


class Player(GameSprite):
    """Provides basic operations of a player such as movement according to
    keystate.
    """
    def __init__(self, stage, earth, player_number):
        GameSprite.__init__(self, stage, earth)
        self.keystate = [False] * 5
        self.cooldown = 0
        self.health = 100

    def get_image(self):
        if self.earth:
            return Resources.earth_player_image
        else:
            return Resources.alien_player_image

    def update(self, dt):
        self.x += (self.keystate[3] - self.keystate[2]) * 200 * dt
        self.y += (self.keystate[0] - self.keystate[1]) * 200 * dt
        self.keep_onscreen()
        self.cooldown = self.cooldown - dt
        if self.keystate[4] and self.cooldown <= 0:
            self.cooldown = 0.125
            bullet_pos = (self.hcenter, self.vcenter)
            Bullet(self.stage, self.earth, bullet_pos, (0, 500))

    def on_key(self, direction, pressed):
        """Call this when a key is pressed which corresponds to the player's
        controls.

        Keyword arguments:
        direction -- UP, DOWN, LEFT, RIGHT or SPACE depending on which key was
                     pressed relative to the player's controls
        pressed   -- True if the key is pressed, False if it is released
        """
        if direction == key.UP:
            self.keystate[0] = pressed
        elif direction == key.DOWN:
            self.keystate[1] = pressed
        elif direction == key.LEFT:
            self.keystate[2] = pressed
        elif direction == key.RIGHT:
            self.keystate[3] = pressed
        elif direction == key.SPACE:
            self.keystate[4] = pressed

    def hit(self):
        self.health -= 1
        self.stage.score -= 1
        if self.health <= 0:
            self.health = 100
            self.x = 0
            self.y = 0
            self.stage.lives -= 1

    def __getstate__(self):
        state = GameSprite.__getstate__(self)
        del state['keystate']
        return state

    def __setstate__(self, state):
        GameSprite.__setstate__(self, state)
        self.keystate = [False] * 5
