import pyglet
from pyglet.window import key

from g.one.resources import Resources
from g.one.sprite import GameSprite


class Ship(GameSprite):
    def __init__(self, stage, player):
        GameSprite.__init__(self, stage, Resources.ship_image)
        self.player = player
        self.keystate = [False] * 4
        d = {("player" + str(player)): self.on_key}
        stage.push_handlers(**d)

    def update(self, dt):
        self.x += (self.keystate[3] - self.keystate[2]) * 200 * dt
        self.y += (self.keystate[0] - self.keystate[1]) * 200 * dt
        self.keep_onscreen()

    def on_key(self, direction, pressed):
        if direction == key.UP:
            self.keystate[0] = pressed
        elif direction == key.DOWN:
            self.keystate[1] = pressed
        elif direction == key.LEFT:
            self.keystate[2] = pressed
        elif direction == key.RIGHT:
            self.keystate[3] = pressed
