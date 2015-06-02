import pyglet
from pyglet.window import key

from g.one.pause_menu import PauseMenu
from g.one.player import Player
from g.one.resources import Resources
from g.one.options import Options


class Game(pyglet.event.EventDispatcher):
    def __init__(self, window, play_as, difficulty, players=1):
        window.push_handlers(self)
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.pause_menu = None
        self.players = []
        for i in range(1, players+1):
            self.players.append(Player(self, i))

    def draw(self):
        if self.paused:
            self.pause_menu.draw()
        else:
            self.batch.draw()

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
        self.window.remove_handlers(self)
        self.change_pause(None)
        for player in self.players:
            player.delete()
        del self.players
        try:
            while True:
                self.pop_handlers()
        except AssertionError:
            pass

    @property
    def paused(self):
        return self.pause_menu is not None
