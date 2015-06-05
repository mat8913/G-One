import pyglet

from g.one.enemy import Enemy


class EnemySpawner():
    def __init__(self, game, earth):
        self.game = game
        self.cooldown = 0
        self.count = 0
        self.earth = earth
        pyglet.clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        self.cooldown -= dt

    def spawn(self, amount):
        pass


class Level1Spawner(EnemySpawner):
    def spawn(self, amount):
        if self.cooldown <= 0 and amount < 6:
            self.cooldown = 1
            self.count += 1
            if self.count < 10:
                return [
                         Enemy(self.game, self.earth, (-1, 400), (100, 0)),
                       ]
            if self.count < 20:
                return [
                         Enemy(self.game, self.earth, (-1, 400), (100, 0)),
                         Enemy(self.game, self.earth, (854, 450), (-100, 0))
                       ]
            if self.count < 21:
                if amount == 0:
                    return [
                           Enemy(self.game, self.earth, (-1, 400), (70, -70)),
                           Enemy(self.game, self.earth, (854, 400), (-70, -70))
                           ]
                else:
                    self.count -= 1
                    return []
            if self.count < 30:
                return [
                         Enemy(self.game, self.earth, (-1, 400), (70, -70)),
                         Enemy(self.game, self.earth, (854, 400), (-70, -70))
                       ]
            return None
        else:
            return []
