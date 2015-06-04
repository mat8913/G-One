import pyglet


class Healthbar():
    def __init__(self, sprite, x=0, y=0):
        self.vlist = pyglet.graphics.vertex_list(
                4,
                ('v2i', (x, 0, x, y, x+10, 0, x+10, y)),
                ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0))
            )
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self):
        self.set_health(self.sprite.health)
        self.vlist.draw(pyglet.gl.GL_TRIANGLE_STRIP)

    def set_health(self, health):
        self.vlist.vertices[1] = self.y+health
        self.vlist.vertices[5] = self.y+health

    def __del__(self):
        self.vlist.delete()
