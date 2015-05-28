import pickle
import os

from pyglet.resource import get_settings_path
from pyglet.window import key


class Options():
    filename = get_settings_path("g-one") + "/options.p"

    default_controls = [
      {
        key.UP:    key.UP,
        key.RIGHT: key.RIGHT,
        key.DOWN:  key.DOWN,
        key.LEFT:  key.LEFT,
        key.SPACE: key.SPACE
      },
      {
        key.UP:    key.W,
        key.RIGHT: key.D,
        key.DOWN:  key.S,
        key.LEFT:  key.A,
        key.SPACE: key.LSHIFT
      }
    ]

    default_options = {
      'fullscreen': False,
      'music': 100,
      'sound effects': 100,
      'controls': default_controls
    }

    @staticmethod
    def load():
        Options.options = Options.options_from_file(Options.filename)
        if Options.options is None:
            Options.options = Options.default_options

    @staticmethod
    def save():
        Options.options_to_file(Options.filename)

    @staticmethod
    def options_from_file(filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    @staticmethod
    def options_to_file(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            pickle.dump(Options.options, f)
