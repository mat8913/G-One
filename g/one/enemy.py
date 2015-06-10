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
    """This is the abstract enemy class.

    It provides basic functionality of enemies such as health and movement
    according the current velocity.

    Subclass this to provide different types of enemies.
    """
    def __init__(self, stage, pos=(0, 0), vel=(0, 0), health=0):
        """Keyword arguments:

        stage  -- the stage this enemy belongs to
        pos    -- tuple of the enemy's initial position
        vel    -- tuple of the enemy's initial velocity
        health -- the enemy's initial health
        """
        GameSprite.__init__(self, stage, not stage.earth)
        self.rotation = 180
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.health = health

    def get_image(self):
        return Resources.ship_image

    def update(self, dt):
        """Update method called every (1/60) seconds.  Makes the enemy move
        according to velocity, bounce if it touches the edge of the screen and
        cause mutual damage if it touches a player.

        Override this method when subclassing but call it at the END of the
        overriding method.
        """
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        self.bounce()
        collision = self.collide_once(self.stage.players)
        if collision is not None:
            self.hit()
            collision.hit()

    def hit(self):
        """Called when the enemy is hit by a bullet or player.

        Causes the enemy to lose health and get deleted when health reaches
        zero.
        """
        self.health -= 1
        if self.health <= 0:
            self.delete()

    def delete(self):
        """Called when the enemy is to be deleted.

        Informs the stage that the enemy is to be deleted from the enemy list
        and then runs GameSprite's delete method.
        """
        self.stage.delete_enemy(self)
        GameSprite.delete(self)


class BasicEnemy(Enemy):
    def __init__(self, stage, pos=(0, 0), vel=(0, 0)):
        Enemy.__init__(self, stage, pos, vel, 5)
        self.cooldown = 0

    def update(self, dt):
        self.cooldown = self.cooldown - dt
        if self.cooldown <= 0:
            self.cooldown = 0.8
            bullet_pos = (self.hcenter, self.vcenter)
            Bullet(self.stage, self.earth, bullet_pos, (0, -500))
        Enemy.update(self, dt)


class HorizontalTrackerEnemy(Enemy):
    def __init__(self, stage, ypos=0, yvel=0, player=None):
        if player is None:
            player = stage.get_target()
        Enemy.__init__(self, stage, (player.hcenter, ypos), (0, yvel),
                       10)
        self.player = player

    def update(self, dt):
        self.hcenter = self.player.hcenter
        Enemy.update(self, dt)
