# This file is part of G-One.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pyglet

from g.one.options import Options


class SoundEffect(pyglet.media.Player):
    """Works the same way as pyglet.media.Player, merely extends its
    functionality:

    * Deletes itself when the sound is complete
    * Sets its own volume according the options
    """
    def __init__(self, sound):
        pyglet.media.Player.__init__(self)
        self.volume = Options.options['sound effects'] / 100
        self.queue(sound)
        self.play()

    def on_player_eos(self):
        self.delete()
