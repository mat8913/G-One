import pyglet
from pyglet.image.codecs.png import PNGImageDecoder

class Resources():
    ship_image = None

    @staticmethod
    def init():
        pyglet.resource.path = ['@g.one.resources']
        pyglet.resource.reindex()

        f = pyglet.resource.file('ship.png')
        Resources.ship_image = pyglet.image.load('ship.png', file=f, decoder=PNGImageDecoder())
        f.close()
