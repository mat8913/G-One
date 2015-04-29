import pyglet
from pyglet.window import key

from g.one.game import Game

class MainMenu():
    def __init__(self, window):
        window.push_handlers(self)
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.selected = 0
        self.title = pyglet.text.Label('G - One',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=427, y=400,
                                  color=(255, 255, 0, 255),
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        option = pyglet.text.Label('One Player',
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=427, y=160,
                                  color=(255, 255, 0, 255),
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        self.options = [option]
        option = pyglet.text.Label('Two Player',
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=427, y=130,
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        self.options += [option]
        option = pyglet.text.Label('Exit',
                                  font_name='Times New Roman',
                                  font_size=16,
                                  x=427, y=100,
                                  anchor_x='center', anchor_y='center',
                                  batch=self.batch)
        self.options += [option]

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.selected = max(self.selected-1, 0)
        elif symbol == key.DOWN:
            self.selected = min(self.selected+1, 2)
        elif symbol == key.ENTER:
            if self.selected == 0:
                self.window.change_stage(Game(self.window, 1))
            elif self.selected == 1:
                self.window.change_stage(Game(self.window, 2))
            elif self.selected == 2:
                quit()
        for (i, option) in enumerate(self.options):
            if self.selected == i:
                option.color = color=(255, 255, 0, 255)
            else:
                option.color = color=(255, 255, 255, 255)

    def draw(self):
        self.batch.draw()
