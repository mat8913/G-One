import pyglet
from pyglet.window import key

from g.one.resources import Resources
from g.one.sprite import GameSprite

class Ship(GameSprite):
    def __init__(self,window,player):
        GameSprite.__init__(self, window, Resources.ship_image)
        self.player = player
        self.keystate = [False] * 4
        if player == 1:
            window.push_handlers(player1=self.on_key)
        elif player == 2:
            window.push_handlers(player2=self.on_key)

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
