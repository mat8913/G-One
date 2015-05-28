import pyglet

from g.one.resources import Resources
from g.one.game_window import GameWindow
from g.one.options import Options


def main():
    Resources.init()
    Options.load()
    window = GameWindow()
    pyglet.app.run()
