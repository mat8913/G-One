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
        self.rotation = 90 - math.degrees(math.atan2(vel[1], vel[0]))
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


class ChaosBullet(Bullet):
    def update(self, dt):
        if self.bounce():
            self.rotation = 90 - math.degrees(math.atan2(self.vel[1],
                                                         self.vel[0]))
        Bullet.update(self,dt)
