import pyglet
from g.one.resources import Resources
from g.one.game_window import GameWindow

def main():
    Resources.init()
    window = GameWindow()
    pyglet.app.run()
