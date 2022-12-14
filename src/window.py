# window.py
#
# Copyright 2022 Lucas Campos Vieira
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Adw

from .widgets.file_chooser import FileChooser
from .player import Player


@Gtk.Template(resource_path='/com/github/lucasscvvieira/Play/window.ui')
class PlayWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PlayWindow'

    view_stack = Gtk.Template.Child()
    player_frame = Gtk.Template.Child()
    open_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view_stack.set_visible_child_name('main')

        self.player = Player()
        self.player_frame.set_child(self.player.widget)

        self.open_button.connect('clicked', self.on_open_button_clicked)

    def on_open_button_clicked(self, widget):
        dialog = FileChooser(self)
        dialog.connect('response', self.on_file_opened)
        dialog.show()

    def on_file_opened(self, widget: Gtk.Widget, response: Gtk.ResponseType):
        filepath = ''
        if response == Gtk.ResponseType.OK:
            filepath = widget.get_file().get_path()

        widget.close()

        if filepath:
            self.view_stack.set_visible_child_name('player')
            self.player.load(filepath)

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent: Gtk.Widget):
        super().__init__()
        self.props.program_name = 'play'
        self.props.version = "0.1.0"
        self.props.authors = ['Lucas Campos Vieira']
        self.props.copyright = '2022 Lucas Campos Vieira'
        self.props.logo_icon_name = 'com.github.lucasscvvieira.Play'
        self.props.modal = True
        self.set_transient_for(parent)
