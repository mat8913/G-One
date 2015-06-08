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

from g.one.enemy import BasicEnemy, HorizontalTrackerEnemy


class EnemySpawner():
    def __init__(self, game):
        self.game = game
        self.cooldown = 0
        self.count = 0
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        if not self.game.paused:
            self.cooldown -= dt

    def spawn(self, amount):
        pass


class Level1Spawner(EnemySpawner):
    def spawn(self, amount):
        if self.cooldown <= 0 and amount < 6:
            self.cooldown = 1
            self.count += 1
            rightmoving = [self.game, (0, 400), (100, 0)]
            leftmoving = [self.game, (854, 400), (-100, 0)]
            rightbouncing = [self.game, (0, 400), (70, -70)]
            leftbouncing = [self.game, (854, 400), (-70, -70)]
            tracking = [self.game, 400, -70]
            if self.count < 10:
                return [
                         BasicEnemy(*rightmoving)
                       ]
            if self.count < 20:
                return [
                         BasicEnemy(*rightmoving),
                         BasicEnemy(*leftmoving)
                       ]
            if self.count < 21:
                if amount == 0:
                    return [
                           BasicEnemy(*rightbouncing),
                           BasicEnemy(*leftbouncing)
                           ]
                else:
                    self.count -= 1
                    return []
            if self.count < 30:
                return [
                         BasicEnemy(*rightbouncing),
                         BasicEnemy(*leftbouncing),
                         HorizontalTrackerEnemy(*tracking)
                       ]
            return None
        else:
            return []
