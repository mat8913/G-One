import pyglet

from g.one.resources import Resources

class GameSprite(pyglet.sprite.Sprite):
    def __init__(self, window, img):
        pyglet.sprite.Sprite.__init__(self, img=img, batch=Resources.batch)
        pyglet.clock.schedule_interval(self.__update, 1/60)
        self.window = window

    def __get_left(self):
        return self.x
    left = property(__get_left)

    def __get_right(self):
        return self.x + self.image.width
    right = property(__get_right)

    def __get_top(self):
        return self.y + self.image.height
    top = property(__get_top)

    def __get_bottom(self):
        return self.y
    bottom = property(__get_bottom)

    def __update(self, dt):
        if self.window.paused:
            return
        self.update(dt)

    def update(self,dt):
        pass

    def intersect(self, sprite):
        return not ((self.left > sprite.right)
            or (self.right < sprite.left)
            or (self.top < sprite.bottom)
            or (self.bottom > sprite.top))

    def collide_once(self, sprite_list):
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite
        return None
