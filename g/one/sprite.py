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
    """This is the abstract game sprite class.

    It provides the basic functionality of sprites used during a game such as
    collision detection and bouncing.

    Subclass this for any sprites which will be used during a game.
    """
    def __init__(self, stage, img):
        """Initialises the sprite and sets up the update method to be called
        every (1/60) seconds.  Causes the image to be anchored to its center.


        Keyword arguments:
        stage -- the stage this sprite belongs to
        img   -- the image to be drawn for this sprite
        """
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        pyglet.sprite.Sprite.__init__(self, img=img, batch=stage.batch)
        pyglet.clock.schedule_interval(self.__update, 1/60)
        self.stage = stage

    def delete(self):
        """Called when the sprite is to be deleted.

        Stops the update method from being called and then calls the pyglet
        Sprite delete method.
        """
        pyglet.clock.unschedule(self.__update)
        pyglet.sprite.Sprite.delete(self)

    def __update(self, dt):
        """Calls the proper update method if the game is not paused.  Do NOT
        override this method when subclassing.  Instead, override the update
        method below.
        """
        if self.stage.paused:
            return
        self.update(dt)

    def update(self, dt):
        """Called every (1/60) seconds if the game is not paused.  Override
        this method when subclassing.
        """
        pass

    def intersect(self, sprite):
        """Determines whether this sprite intersects with the given sprite.
        Returns a boolean.
        """
        return not ((self.left > sprite.right) or
                    (self.right < sprite.left) or
                    (self.top < sprite.bottom) or
                    (self.bottom > sprite.top))

    def collide_once(self, sprite_list):
        """Returns the first sprite in the sprite_list that this sprite
        intersects with.  If this sprite does not intersect with any sprites in
        the sprite list, returns None.
        """
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite
        return None

    def onscreen(self):
        """Determines whether this sprite is onscreen.  This will return True
        even if the sprite is only partially onscreen.
        """
        return not (self.right < 0 or
                    self.left > 854 or
                    self.top < 0 or
                    self.bottom > 480)

    def keep_onscreen(self):
        """Moves this sprite entirely onscreen.  Returns a list of the
        directions the sprite was offscreen or an empty list if none.  The
        sprite will be moved even if it was only partially offscreen.
        """
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
        """Determines the direction from this sprite to the given coordinates.
        ords should be a tuple.  Returns a normalised vector as a tuple.
        """
        x = ords[0] - self.hcenter
        y = ords[1] - self.vcenter
        magnitude = math.sqrt(x*x + y*y)
        return tuple(a / magnitude for a in (x, y))

    def direction_to_sprite(self, sprite):
        """Determines the direction from this sprite to the given sprite.
        Returns a normalised vector as a tuple.
        """
        return self.direction_to_ords((sprite.hcenter, sprite.vcenter))

    def bounce(self):
        """Alters this sprite's velocity causing it to bounce if it was at the
        screen edge.  Returns True if the sprite did bounce or False if no
        action was taken.

        Note: self.vel must be defined as this sprite's velocity.
        """
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

    # The properties below are self-explanatory, keeping in mind that self.x
    # and self.y point to the center of the sprite.

    @property
    def left(self):
        return self.x - self.image.width/2

    @left.setter
    def left(self, value):
        self.x = value + self.image.width/2

    @property
    def right(self):
        return self.x + self.image.width/2

    @right.setter
    def right(self, value):
        self.x = value - self.image.width/2

    @property
    def hcenter(self):
        return self.x

    @hcenter.setter
    def hcenter(self, value):
        self.x = value

    @property
    def top(self):
        return self.y + self.image.height/2

    @top.setter
    def top(self, value):
        self.y = value - self.image.height/2

    @property
    def bottom(self):
        return self.y - self.image.height/2

    @bottom.setter
    def bottom(self, value):
        self.y = value + self.image.height/2

    @property
    def vcenter(self):
        return self.y

    @vcenter.setter
    def vcenter(self, value):
        self.y = value
