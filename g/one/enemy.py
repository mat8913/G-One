import math

from g.one.resources import Resources
from g.one.sprite import GameSprite
from g.one.bullet import Bullet


class Enemy(GameSprite):
    def __init__(self, stage, earth, pos, vel):
        GameSprite.__init__(self, stage, Resources.ship_image)
        self.rotation = 180
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.cooldown = 0
        self.earth = earth
        self.health = 5

    def update(self, dt):
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        self.cooldown = self.cooldown - dt
        if self.cooldown <= 0:
            self.cooldown = 0.5
            bullet_pos = (self.hcenter, self.vcenter)
            Bullet(self.stage, self.earth, bullet_pos, (0, -500))
        self.bounce()
        collision = self.collide_once(self.stage.players)
        if collision is not None:
            self.hit()
            collision.hit()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.delete()

    def delete(self):
        self.stage.delete_enemy(self)
        GameSprite.delete(self)
