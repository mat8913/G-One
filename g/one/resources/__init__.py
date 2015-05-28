import pyglet
from pyglet.image.codecs.png import PNGImageDecoder


class Resources():
    @staticmethod
    def init():
        pyglet.resource.path = ['@g.one.resources']
        pyglet.resource.reindex()
        Resources.ship_image = Resources.load_image("ship.png")

    def load_image(filename):
        with pyglet.resource.file(filename) as f:
            decoder = PNGImageDecoder()
            return pyglet.image.load(filename, file=f, decoder=decoder)
