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
            textbuffer = self.textview.get_buffer()
            textbuffer.set_text(the_file.read(MAX_BUFFER_SIZE))
            self.text_start_iter = textbuffer.get_start_iter()
            self.typing_end_iter = textbuffer.get_start_iter()
            self.buffer_end_iter = textbuffer.get_end_iter()
            the_file.close()

            colormap = self.textview.get_colormap()
            color = colormap.alloc_color(0xffff, 0xffff, 0xffff)
            tag = self.textview.get_buffer().create_tag("fg_white", foreground_gdk=color)
            color = colormap.alloc_color(0, 0, 0)
            tag = self.textview.get_buffer().create_tag("fg_black", foreground_gdk=color)
        chooser.destroy()

    def newline(self):
        # Advance the text buffer's iterator by one line.
        # Currently, text does not start to scroll until the first
        # off-screen line is reached.
        self.textview.forward_display_line(self.typing_end_iter)
        print self.typing_end_iter.get_line()
        self.textview.scroll_to_iter(self.typing_end_iter, 0)

    def is_forbidden_key_press(self, event):
        return (
            not hasattr(event, "string") or
            event.string == "" or
            event.state & gtk.gdk.CONTROL_MASK or
            event.state & gtk.gdk.MOD1_MASK )
            
    def on_text_entry(self, widget, event):
        # Let the user see responses to normal typing including
        # the Enter key and backspace, but nothing else.
        # Cut-and-paste and the arrow keys should do nothing.

        if event.keyval == 65288: # Was backspace key pressed?
            # Was the last typed character a newline?
            if len(self.typed_buffer) > 0 and self.typed_buffer[-1] != "\n":
                # It is safe to delete the last character.
                self.typed_buffer = self.typed_buffer[0:-1]
                self.typing_end_iter.backward_char()
            else:
                # Don't delete past beginning of current line.
                return True
        elif event.keyval == 65293: # Was enter key pressed?
            self.newline()
            self.typed_buffer += "\n"
            self.typing_end_iter.forward_char()
        elif self.is_forbidden_key_press(event):
            return True
        else:
            self.typed_buffer += event.string
            self.typing_end_iter.forward_char()
        print self.typed_buffer
        self.textview.get_buffer().remove_tag_by_name(
                "fg_white", self.typing_end_iter, self.buffer_end_iter)
        self.textview.get_buffer().apply_tag_by_name(
                "fg_black", self.typing_end_iter, self.buffer_end_iter)
        self.textview.get_buffer().remove_tag_by_name(
                "fg_black", self.text_start_iter, self.typing_end_iter)
        self.textview.get_buffer().apply_tag_by_name(
                "fg_white", self.text_start_iter, self.typing_end_iter)
        print self.text_start_iter.get_offset()
        print self.typing_end_iter.get_offset()
        print self.buffer_end_iter.get_offset()

    def on_text_view_focus( self, widget, event, data=None ):
        # TextViews should never get the focus. Don't intefere with typing
        self.textentry.grab_focus()
        return True

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

    def init_window( self ):
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
        self.textview.connect("focus", self.on_text_view_focus)
        self.textview.connect("button-press-event", self.on_text_view_focus)

        self.textentry = gtk.TextView()
        self.textentry.set_size_request(300,20)
        self.textentry.connect("key-press-event", self.on_text_entry)

        self.layout = gtk.Layout()
        self.layout.put( self.textview, 0, 0 )
        self.layout.put( self.textentry, 0, 20 )

        self.choose_file = gtk.Button("Load file")
        self.choose_file.connect("clicked", self.load_file, None)

        self.modes = gtk.combo_box_new_text()
        self.modes.append_text("Invisible typing")
        self.modes.append_text("Visible typing")
        self.modes.append_text("Mark mistakes")
        self.modes.append_text("Freeze on mistake")

        self.vbox = gtk.VBox(False)
        self.vbox.pack_start(self.layout, True)
        self.vbox.pack_start(self.choose_file, False)
        self.vbox.pack_start(self.modes, False)

        self.window.add(self.vbox)

    def init_buffers( self ):
        self.typed_buffer = ""
        self.first_press_buffer = ""


    def __init__(self):
        self.init_window()
        self.init_buffers()
        self.window.show_all()

    def main(self):
        gtk.main()



if __name__ == "__main__":
    print __name__
    base = Typerack()
    base.main()
