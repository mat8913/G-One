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
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.image.width

    @right.setter
    def right(self, value):
        self.x = value - self.image.width

    @property
    def top(self):
        return self.y + self.image.height

    @top.setter
    def top(self, value):
        self.y = value - self.image.height

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value

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
        return not (self.left < 0 or
                    self.right > 854 or
                    self.bottom < 0 or
                    self.top > 480)

    def keep_onscreen(self):
        self.left = max(0, self.left)
        self.right = min(854, self.right)
        self.bottom = max(0, self.bottom)
        self.top = min(480, self.top)
