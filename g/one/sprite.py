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
import pyglet

from g.one.resources import Resources


class GameSprite(pyglet.sprite.Sprite):
    def __init__(self, stage, img):
        pyglet.sprite.Sprite.__init__(self, img=img, batch=stage.batch)
        pyglet.clock.schedule_interval(self.__update, 1/60)
        self.stage = stage

    def delete(self):
        pyglet.clock.unschedule(self.__update)
        pyglet.sprite.Sprite.delete(self)

    @property
    def left(self):
        if self.rotation <= 90:
            return self.x
        else:
            return self.x - self.image.width

    @left.setter
    def left(self, value):
        if self.rotation <= 90:
            self.x = value
        else:
            self.x = value + self.image.width

    @property
    def right(self):
        if self.rotation <= 90:
            return self.x + self.image.width
        else:
            return self.x

    @right.setter
    def right(self, value):
        if self.rotation <= 90:
            self.x = value - self.image.width
        else:
            self.x = value

    @property
    def hcenter(self):
        return (self.left+self.right) / 2

    @hcenter.setter
    def hcenter(self, value):
        self.right = value + self.image.width/2

    @property
    def top(self):
        if self.rotation <= 90:
            return self.y + self.image.height
        else:
            return self.y

    @top.setter
    def top(self, value):
        if self.rotation <= 90:
            self.y = value - self.image.height
        else:
            self.y = value

    @property
    def bottom(self):
        if self.rotation <= 90:
            return self.y
        else:
            return self.y - self.image.height

    @bottom.setter
    def bottom(self, value):
        if self.rotation <= 90:
            self.y = value
        else:
            self.y = value + self.image.height

    @property
    def vcenter(self):
        return (self.top+self.bottom) / 2

    @vcenter.setter
    def vcenter(self, value):
        self.bottom = value - self.image.height/2

    def __update(self, dt):
        if self.stage.paused:
            return
        self.update(dt)

    def update(self, dt):
        pass

    def intersect(self, sprite):
        return not ((self.left > sprite.right) or
                    (self.right < sprite.left) or
                    (self.top < sprite.bottom) or
                    (self.bottom > sprite.top))

    def collide_once(self, sprite_list):
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite
        return None

    def onscreen(self):
        return not (self.right < 0 or
                    self.left > 854 or
                    self.top < 0 or
                    self.bottom > 480)

    def keep_onscreen(self):
        ret = []
        if 0 > self.left:
            self.left = 0
            ret += ["left"]
        if 854 < self.right:
            self.right = 854
            ret += ["right"]
        if 0 > self.bottom:
            self.bottom = 0
            ret += ["bottom"]
        if 480 < self.top:
            self.top = 480
            ret += ["top"]
        return ret

    def direction_to_ords(self, ords):
        x = ords[0] - self.hcenter
        y = ords[1] - self.vcenter
        magnitude = math.sqrt(x*x + y*y)
        return tuple(a / magnitude for a in (x, y))

    def direction_to_sprite(self, sprite):
        return self.direction_to_ords((sprite.hcenter, sprite.vcenter))

    def bounce(self):
        ret = False
        dx, dy = self.vel
        offscreen = self.keep_onscreen()
        if "left" in offscreen or "right" in offscreen:
            dx = -dx
            ret = True
        if "top" in offscreen or "bottom" in offscreen:
            dy = -dy
            ret = True
        self.vel = (dx, dy)
        return ret
