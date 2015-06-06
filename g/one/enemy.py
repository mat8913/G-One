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
from g.one.bullet import Bullet


class Enemy(GameSprite):
    def __init__(self, stage, earth, pos, vel, health):
        GameSprite.__init__(self, stage, Resources.ship_image)
        self.rotation = 180
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.earth = earth
        self.health = health

    def update(self, dt):
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        self.bounce()
        collision = self.collide_once(self.stage.players)
        if collision is not None:
            self.hit()
            collision.hit()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.delete()

    def delete(self):
        self.stage.delete_enemy(self)
        GameSprite.delete(self)


class BasicEnemy(Enemy):
    def __init__(self, stage, earth, pos, vel):
        Enemy.__init__(self, stage, earth, pos, vel, 5)
        self.cooldown = 0

    def update(self, dt):
        self.cooldown = self.cooldown - dt
        if self.cooldown <= 0:
            self.cooldown = 0.8
            bullet_pos = (self.hcenter, self.vcenter)
            Bullet(self.stage, self.earth, bullet_pos, (0, -500))
        Enemy.update(self, dt)


class HorizontalTrackerEnemy(Enemy):
    def __init__(self, stage, earth, ypos, yvel, player=None):
        if player is None:
            player = stage.get_target()
        Enemy.__init__(self, stage, earth, (player.hcenter, ypos), (0, yvel),
                       10)
        self.player = player

    def update(self, dt):
        self.hcenter = self.player.hcenter
        Enemy.update(self, dt)
