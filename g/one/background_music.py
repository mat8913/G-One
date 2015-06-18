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


class BackgroundMusic():
    """Player of background music.  Music is looped and correct volume is set
    automatically.  This is a static class.
    """
    @classmethod
    def init(cls):
        """Call this once during initialisation"""
        cls.player = pyglet.media.Player()
        cls.player.push_handlers(cls.on_player_eos)
        cls.music = None
        Options.listeners.append(cls.on_options_changed)
        cls.on_options_changed()

    @classmethod
    def play(cls, music):
        """Plays a music track.  Does nothing if the track is already
        playing."""
        if cls.music == music:
            return
        cls.music = None
        while cls.player.source is not None:
            cls.player.next_source()
        cls.music = music
        cls.player.queue(music)
        cls.player.play()

    @classmethod
    def on_player_eos(cls):
        """Event handler for when the player runs out of music"""
        # Loop the current track if there is one
        if cls.music is None:
            return
        cls.player.queue(cls.music)
        cls.player.play()

    @classmethod
    def on_options_changed(cls):
        """Event handler for when the options change"""
        cls.player.volume = Options.options['music'] / 100
