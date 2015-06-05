import math

from g.one.resources import Resources
from g.one.sprite import GameSprite


class Bullet(GameSprite):
    def __init__(self, stage, earth, pos, vel):
        if earth:
            bullet_image = Resources.earth_bullet_image
        else:
            bullet_image = Resources.alien_bullet_image
        GameSprite.__init__(self, stage, bullet_image)
        self.hcenter, self.vcenter = pos
        self.vel = vel
        self.belong_to_player = earth == stage.earth

    def update(self, dt):
        if self.stage.deleted:
            self.delete()
            return
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        if self.belong_to_player:
            collision = self.collide_once(self.stage.enemies)
        else:
            collision = self.collide_once(self.stage.players)
        if collision is not None:
            collision.hit()
            self.delete()
            return

        if not self.onscreen():
            self.delete()

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel = value
        self.rotation = 90 - math.degrees(math.atan2(value[1], value[0]))


class ChaosBullet(Bullet):
    def update(self, dt):
        self.bounce()
        Bullet.update(self, dt)
