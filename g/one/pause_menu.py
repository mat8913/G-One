import pyglet
from pyglet.window import key

from g.one.menu import Menu
from g.one.menu_item import *


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self)
        self.game = game
        self.title = pyglet.text.Label(
          'Paused',
          font_name='Times New Roman',
          font_size=25,
          x=427, y=400,
          color=(255, 255, 255, 255),
          anchor_x='center', anchor_y='center',
          batch=self.batch
        )
        self.options = [
          MenuAction(self, "Resume", self.resume_pressed, 427, 160),
          MenuItem(self, "Save Game", 427, 130),
          MenuItem(self, "Highscore List", 427, 100),
          MenuAction(self, "Exit", self.exit_pressed, 427, 70),
        ]
        self.selected = 0

    def resume_pressed(self):
        self.game.change_pause(None)

    def exit_pressed(self):
        self.game.exit()

    def delete(self):
        self.options = None
