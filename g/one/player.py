import pyglet
from pyglet.window import key

from g.one.resources import Resources
from g.one.sprite import GameSprite
from g.one.bullet import Bullet


class Player(GameSprite):
    def __init__(self, stage, player_number):
        GameSprite.__init__(self, stage, Resources.ship_image)
        self.keystate = [False] * 5
        self.cooldown = 0

    def update(self, dt):
        self.x += (self.keystate[3] - self.keystate[2]) * 200 * dt
        self.y += (self.keystate[0] - self.keystate[1]) * 200 * dt
        self.keep_onscreen()
        self.cooldown = self.cooldown - dt
        if self.keystate[4] and self.cooldown <= 0:
            self.cooldown = 0.125
            Bullet(self.stage, (self.hcenter, self.vcenter), (0, 500))

    def on_key(self, direction, pressed):
        if direction == key.UP:
            self.keystate[0] = pressed
        elif direction == key.DOWN:
            self.keystate[1] = pressed
        elif direction == key.LEFT:
            self.keystate[2] = pressed
        elif direction == key.RIGHT:
            self.keystate[3] = pressed
        elif direction == key.SPACE:
            self.keystate[4] = pressed
