import math

from g.one.resources import Resources
from g.one.sprite import GameSprite
from g.one.bullet import Bullet


class Enemy(GameSprite):
    def __init__(self, stage, pos, vel):
        GameSprite.__init__(self, stage, Resources.ship_image)
        self.rotation = 180
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.cooldown = 0

    def update(self, dt):
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        self.cooldown = self.cooldown - dt
        if self.cooldown <= 0:
            self.cooldown = 0.5
            bullet_vel = self.direction_to(self.stage.players[0])
            bullet_vel = tuple(x*500 for x in bullet_vel)
            Bullet(self.stage, (self.hcenter, self.vcenter), bullet_vel)
        if self.keep_onscreen():
            self.vel = tuple(-x for x in self.vel)
