import pyglet
from pyglet.window import key

from g.one.pause_menu import PauseMenu
from g.one.player import Player
from g.one.enemy import Enemy
from g.one.resources import Resources
from g.one.options import Options
from g.one.healthbar import Healthbar


class Game(pyglet.event.EventDispatcher):
    def __init__(self, window, earth, difficulty, players=1):
        window.push_handlers(self)
        self.window = window
        self.earth = earth
        self.batch = pyglet.graphics.Batch()
        self.pause_menu = None
        self.players = []
        self.enemies = []
        self.healthbars = []
        self.deleted = False
        self.__target = -1
        for i in range(1, players+1):
            self.players.append(Player(self, self.earth, i))
        for i, e in enumerate(self.players):
            self.healthbars.append(Healthbar(e, 10 * i))
        self.enemies.append(Enemy(self, not earth, (0, 400), (100, 0)))

    def draw(self):
        if self.paused:
            self.pause_menu.draw()
        else:
            self.batch.draw()
            for healthbar in self.healthbars:
                healthbar.draw()

    def on_key_press(self, symbol, modifiers):
        if self.paused:
            return
        if symbol == key.ESCAPE:
            self.pause_menu = PauseMenu(self)
            return
        for i, player in enumerate(self.players):
            for k, v in Options.options['controls'][i].items():
                if symbol == v:
                    player.on_key(k, True)
                    return

    def on_key_release(self, symbol, modifiers):
        if self.paused:
            return self.pause_menu.on_key_release(symbol, modifiers)
        for i, player in enumerate(self.players):
            for k, v in Options.options['controls'][i].items():
                if symbol == v:
                    player.on_key(k, False)
                    return

    def change_pause(self, pause_menu):
        self.pause_menu.delete()
        self.pause_menu = pause_menu

    def exit(self):
        from g.one.menu import MainMenu
        self.window.change_stage(MainMenu(self.window))

    def delete(self):
        self.deleted = True
        self.window.remove_handlers(self)
        self.change_pause(None)
        for player in self.players:
            player.delete()
        del self.players
        while self.enemies:
            self.enemies[0].delete()
        del self.enemies
        try:
            while True:
                self.pop_handlers()
        except AssertionError:
            pass
        del self.healthbars

    @property
    def paused(self):
        return self.pause_menu is not None

    def get_target(self):
        self.__target = self.__target + 1
        if self.__target >= len(self.players):
            self.__target = 0
        return self.players[self.__target]

    def delete_enemy(self, enemy):
        self.enemies.remove(enemy)
