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

import math

from g.one.resources import Resources
from g.one.sprite import GameSprite


class Bullet(GameSprite):
    def __init__(self, stage, earth, pos, vel):
        GameSprite.__init__(self, stage, earth)
        stage.bullets.append(self)
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.belong_to_player = earth == stage.earth

    def get_image(self):
        if self.earth:
            return Resources.earth_bullet_image
        else:
            return Resources.alien_bullet_image

    def update(self, dt):
        if self.stage.deleted:
            self.delete()
            return
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        if self.belong_to_player:
            collision = self.collide_once(self.stage.enemies)
        else:
            collision = self.collide_once(self.stage.players)
        if collision is not None:
            collision.hit()
            if not self.stage.deleted:
                self.delete()
            return

        if not self.onscreen():
            self.delete()

    def delete(self):
        self.stage.delete_bullet(self)
        GameSprite.delete(self)

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel = value
        self.rotation = 90 - math.degrees(math.atan2(value[1], value[0]))


class BouncyBullet(Bullet):
    def __init__(self, *args):
        Bullet.__init__(self, *args)
        self.bounces = 5

    def update(self, dt):
        if self.bounce():
            self.bounces -= 1
        if self.bounces <= 0:
            self.delete()
            return
        Bullet.update(self, dt)


class HomingBullet(Bullet):
    def __init__(self, *args):
        Bullet.__init__(self, *args)
        self.bounces = 5

    def update(self, dt):
        if self.keep_onscreen():
            dx, dy = self.vel
            magnitude = math.sqrt(dx*dx + dy*dy)
            dx, dy = self.direction_to_sprite(self.stage.get_target())
            self.vel = tuple(x*magnitude for x in (dx, dy))
            self.bounces -= 1
        if self.bounces <= 0:
            self.delete()
            return
        Bullet.update(self, dt)
