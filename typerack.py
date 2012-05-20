#!/usr/bin/env python

# typerack - Python Typing Practice
#
# Practice typing content of relevance to you.
#
# Copyright (C) 2012 Justin Hellings <justin.hellings@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require('2.0')
import gtk

# Maximum number of bytes to read in to text buffer.
MAX_BUFFER_SIZE = 1024 * 1024


class Typerack :

    def load_file(self, widget, data=None):
        # Create a file dialog
        chooser = gtk.FileChooserDialog(
                title=None,
                action=gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons=(
                    gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OPEN, gtk.RESPONSE_OK
                    )
                )

        # Show the dialog to the user
        response = chooser.run()

        # Did the user select a file?
        if response == gtk.RESPONSE_OK :

            # Load text from the file.
            the_file = open( chooser.get_filename(), 'r' )
            self.textview.get_buffer().set_text(the_file.read(MAX_BUFFER_SIZE))
            self.textiter = self.textview.get_iter_at_location(0,0)
            the_file.close()

        chooser.destroy()

    def newline(self, widget, event, data=None):
        # Advance the text buffer's iterator by one line.
        # Currently, text does not start to scroll until the first
        # off-screen line is reached.
        self.textview.forward_display_line(self.textiter)
        print self.textiter.get_line()
        self.textview.scroll_to_iter(self.textiter, 0)

    def delete_event(self, widget, event, data=None):
        # Counter-intuitively, return FALSE to terminate
        # or TRUE to cancel termination
        # Aha! This is because TRUE indicates that an event has
        # been handled whereas FALSE indicates that it has not.
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()
        # Should we be returning a boolean here to indicate
        # that the event has been handled?

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # delete_event is a signal sent by the window manager
        self.window.connect("delete_event", self.delete_event)

        # destroy is sent after returning FALSE from
        # our delete_event handler
        self.window.connect("destroy", self.destroy)

        self.window.set_border_width(10)
        self.window.set_resizable(True)
        self.window.set_default_size(300,300)

        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_size_request(300,300)

        # For now, using mouse clicks on the TextView to test
        # scrolling through the file.
        self.textview.connect("button-press-event", self.newline, None)

        self.textentry = gtk.TextView()
        self.textentry.set_size_request(300,20)
        self.textentry.get_buffer().set_text("How now brown cow?")

        self.layout = gtk.Layout()
        self.layout.put( self.textview, 0, 0 )
        self.layout.put( self.textentry, 0, 20 )

        self.button = gtk.Button("Load file")
        self.button.connect("clicked", self.load_file, None)

        self.vbox = gtk.VBox(False)
        self.vbox.pack_start(self.layout, True)
        self.vbox.pack_start(self.button, False)

        self.window.add(self.vbox)
        self.window.show_all()

    def main(self):
        gtk.main()



if __name__ == "__main__":
    print __name__
    base = Typerack()
    base.main()
