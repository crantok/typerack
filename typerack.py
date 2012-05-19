#!/usr/bin/env python

# example base.py

import pygtk
pygtk.require('2.0')
import gtk

MAX_BUFFER_SIZE = 1024 * 1024


class HelloWorld:

    def hello(self, widget, data=None):
        print "Hello World"
        chooser = gtk.FileChooserDialog(
                title=None,
                action=gtk.FILE_CHOOSER_ACTION_OPEN,
                buttons=(
                    gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OPEN, gtk.RESPONSE_OK
                    )
                )
        response = chooser.run()
        if response == gtk.RESPONSE_OK :
            the_file = open( chooser.get_filename(), 'r' )
            self.textview.get_buffer().set_text(the_file.read(MAX_BUFFER_SIZE))
            self.textiter = self.textview.get_iter_at_location(0,0)
            the_file.close()

        chooser.destroy()

    def goodbye(self, widget, event, data=None):
        self.textview.forward_display_line(self.textiter)
        print self.textiter.get_line()
        self.textview.scroll_to_iter(self.textiter, 0)

    def delete_event(self, widget, event, data=None):
        # Counter-intuitively, return FALSE to terminate
        # or TRUE to cancel termination
        # Aha! This is because TRUE indicates that an event has
        # been handled whereas FALSE indicates that it has not.
        print "delete event occurred"
        # Shows a gtk.Window object. Emmitter or catcher?
        print widget
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()
        # Shows a gtk.Window object. Emmitter or catcher?
        print widget
        # Should we be returning a boolean here to indicate
        # that the event has been handled?

    def __init__(self):
        print __name__
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
        self.textview.connect("button-press-event", self.goodbye, None)
        self.textview.set_size_request(300,300)

        self.textentry = gtk.TextView()
        self.textentry.set_size_request(300,20)
        self.textentry.get_buffer().set_text("How now brown cow?")

        self.layout = gtk.Layout()
        self.layout.put( self.textview, 0, 0 )
        self.layout.put( self.textentry, 0, 20 )

        self.button = gtk.Button("Yo!")
        self.button.connect("clicked", self.hello, None)

        self.vbox = gtk.VBox(False)
        self.vbox.pack_start(self.layout, True)
        self.vbox.pack_start(self.button, False)

        # Interesting - The button will destroy the window
        # when clicked. This sends the same signal to the
        # window that would be sent by returning FALSE from
        # the delete_event handler.
        # More interesting - is gtk.Widget.destroy a class method
        # or is it an instance method?
        # class, whereas connect() accepts
        # self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        # Trying this instead gives this error:
        #    TypeError: destroy() takes no arguments (1 given)
        # self.button.connect("clicked", self.window.destroy)

        self.window.add(self.vbox)
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    print __name__
    # Looks like Python doesn't use a "new" operator or method.
    base = HelloWorld()
    base.main()
