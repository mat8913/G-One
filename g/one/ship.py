from g.one.resources import Resources
from pyglet.window import key
import pyglet

class Ship(pyglet.sprite.Sprite):
    vel_y = 0

    # [up, down, left, right]
    keystate = [False] * 4

    def __init__(self, parent):
        pyglet.sprite.Sprite.__init__(self, img=Resources.ship_image,
                                      batch=Resources.batch)
        pyglet.clock.schedule_interval(self.update, 1/60)
        parent.push_handlers(player1=self.on_key)

    def update(self,dt):
        self.x += (self.keystate[3] - self.keystate[2]) * 200 * dt
        self.y += (self.keystate[0] - self.keystate[1]) * 200 * dt

    def on_key(self, direction, pressed):
        if direction == key.UP:
            self.keystate[0] = pressed
        elif direction == key.DOWN:
            self.keystate[1] = pressed
        elif direction == key.LEFT:
            self.keystate[2] = pressed
        elif direction == key.RIGHT:
            self.keystate[3] = pressed
