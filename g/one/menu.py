import pyglet
from pyglet.window import key

from g.one.menu_item import *
from g.one.game import Game


class Menu():
    def __init__(self, window):
        window.push_handlers(self)
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self._selected = 0
        self.options = []

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.DOWN:
            self.selected = min(self.selected+1, len(self.options)-1)
        else:
            self.options[self.selected].on_key_release(symbol, modifiers)

    def draw(self):
        self.batch.draw()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self.options[self._selected].set_selected(False)
        self._selected = value
        self.options[self._selected].set_selected(True)

    def delete(self):
        self.window.remove_handlers(self)
        self.options = None


class MainMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label(
          'G - One',
          font_name='Times New Roman',
          font_size=36,
          x=427, y=400,
          color=(255, 255, 0, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = [
          MenuAction(self, "New Game", self.new_game_pressed, 427, 160),
          MenuItem(self, "Load Game", 427, 130),
          MenuItem(self, "Highscore List", 427, 100),
          MenuItem(self, "Options", 427, 70),
          MenuAction(self, "Exit", quit, 427, 40)
        ]
        self.selected = 0

    def new_game_pressed(self):
        self.window.change_stage(NewGameMenu(self.window))



class NewGameMenu(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.title = pyglet.text.Label('G - One',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=427, y=400,
                                  color=(255, 255, 0, 255),
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        self.options.append(MenuItem(self, "New Game", 427, 160))
        self.options.append(MenuItem(self, "Load Game", 427, 130))
        self.options.append(MenuItem(self, "Highscore List", 427, 100))
        self.options.append(MenuItem(self, "Options", 427, 70))
        tmp = []
        tmp.append(MenuAction(self, "Back", lambda: window.change_stage(MainMenu(window)), 100, 40))
        tmp.append(MenuAction(self, "Start", lambda: window.change_stage(Game(window)), 754, 40))
        self.options.append(HorizontalSelection(tmp))
        self.selected = 0
