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
from g.one.bullet import *
from g.one.sound_effect import SoundEffect


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
        if stage.difficulty == 1:
            self.health *= 2

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
            collision.hit()

    def hit(self):
        """Called when the enemy is hit by a bullet or player.

        Causes the enemy to lose health and get deleted when health reaches
        zero.
        """
        self.health -= 1
        self.stage.score += 1
        if self.health <= 0:
            SoundEffect(Resources.explosion_sound)
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

    def get_image(self):
        if self.earth:
            return Resources.earth_player_image
        else:
            return Resources.alien_player_image

    def update(self, dt):
        self.cooldown = self.cooldown - dt
        if self.cooldown <= 0:
            self.cooldown = 0.8
            bullet_pos = (self.hcenter, self.vcenter)
            if self.stage.difficulty == 1:
                bullet_vel = tuple(
                  500*x for x in
                  self.direction_to_sprite(self.stage.get_target())
                )
                BouncyBullet(self.stage, self.earth, bullet_pos, bullet_vel)
            else:
                Bullet(self.stage, self.earth, bullet_pos, (0, -500))
        Enemy.update(self, dt)


class HorizontalTrackerEnemy(Enemy):
    def __init__(self, stage, ypos=0, yvel=0, player=None):
        if player is None:
            player = stage.get_target()
        Enemy.__init__(self, stage, (player.hcenter, ypos), (0, yvel),
                       10)
        self.player = player
        self.cooldown = 0

    def update(self, dt):
        self.hcenter = self.player.hcenter
        Enemy.update(self, dt)
        self.cooldown -= dt
        if self.cooldown <= 0 and self.stage.difficulty == 1:
            self.cooldown = 0.8
            bullet_pos = (self.hcenter, self.vcenter)
            Bullet(self.stage, self.earth, bullet_pos, (0, -500))

    def get_image(self):
        if self.earth:
            return Resources.earth_tracker_image
        else:
            return Resources.alien_tracker_image


class SplitterEnemy(Enemy):
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

    def hit(self):
        self.health -= 1
        self.stage.score += 1
        if self.health <= 0:
            new_vel = (-self.vel[1], self.vel[0])
            new_enemy = SplitterEnemy(self.stage, (self.x, self.y), new_vel)
            self.stage.enemies.append(new_enemy)

            new_vel = (self.vel[1], -self.vel[0])
            new_enemy = SplitterEnemy(self.stage, (self.x, self.y), new_vel)
            self.stage.enemies.append(new_enemy)

            SoundEffect(Resources.explosion_sound)
            self.delete()

    def get_image(self):
        if self.earth:
            return Resources.earth_splitter_image
        else:
            return Resources.alien_splitter_image
