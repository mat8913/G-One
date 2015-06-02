import math

from g.one.resources import Resources
from g.one.sprite import GameSprite


class Bullet(GameSprite):
    def __init__(self, stage, pos, vel):
        GameSprite.__init__(self, stage, Resources.bullet_image)
        self.x, self.y = pos
        self.vel = vel
        self.rotation = 90 - math.degrees(math.atan2(vel[1], vel[0]))

    def update(self, dt):
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        if not self.onscreen():
            self.delete()
