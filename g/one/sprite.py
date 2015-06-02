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
        self.x = value - self.image.width/2

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
        self.y = value - self.image.height/2

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
        self.left = max(0, self.left)
        self.right = min(854, self.right)
        self.bottom = max(0, self.bottom)
        self.top = min(480, self.top)
