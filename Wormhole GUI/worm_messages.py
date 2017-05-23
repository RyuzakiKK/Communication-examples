import gi
import wormhole_functions as worm
import logging
from twisted.internet import reactor
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

logger = logging.getLogger(__name__)

class GUI:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('window.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("main_window")
        self.window.show()

        self.notebook = self.builder.get_object("notebook")
        sp2 = self.builder.get_object("send_panel_2")
        self.notebook.prepend_page(sp2, Gtk.Label("Send"))
        sp2.hide()

        text_buffer = self.builder.get_object("code_to_send").get_buffer()
        text_buffer.connect('changed', self.on_code_text_changed)

        # Start the reactor in another thread
        t = threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0})
        t.start()

    @staticmethod
    def on_delete_window(*args):
        reactor.callFromThread(reactor.stop)
        Gtk.main_quit(*args)

    def on_code_text_changed(self, entryObject, *args):
        send_button = self.builder.get_object("send_button")
        # Check if the code field is not empty
        if len(entryObject.get_text(*entryObject.get_bounds(), False)) > 0:
            send_button.set_sensitive(True)
        else:
            send_button.set_sensitive(False)

    def on_send_pressed(self, button):
        # Hide the panel 1 and display the panel 2
        sp2 = self.builder.get_object("send_panel_2")
        sp2.show()
        self.notebook.set_current_page(0)
        sp1 = self.builder.get_object("send_panel_1")
        sp1.hide()

        text_buffer = self.builder.get_object("code_to_send").get_buffer()

        # text_buffer.get_bounds() means "get the entire message"
        code = text_buffer.get_text(*text_buffer.get_bounds(), False)
        text_buffer = self.builder.get_object("text_to_send").get_buffer()
        message = text_buffer.get_text(*text_buffer.get_bounds(), False)
        if message == "":
            message = "Hello World :)"

        finish_label = self.builder.get_object("finish_label")
        finish_label.set_text("Sending the message")

        worm.send(code, message, self.on_message_callback)

    def on_stop_send_clicked(self, button):
        worm.stop_sending(self.on_stop_send_callback)

    def on_stop_send_callback(self):
        finish_label = self.builder.get_object("finish_label")
        finish_label.set_text("Sending cancelled")
        finish_button = self.builder.get_object("finish_send_button")
        finish_button.set_sensitive(True)
        stop_button = self.builder.get_object("stop_send_button")
        stop_button.set_sensitive(False)

    def on_message_callback(self, completed):
        finish_button = self.builder.get_object("finish_send_button")
        finish_button.set_sensitive(True)
        stop_button = self.builder.get_object("stop_send_button")
        stop_button.set_sensitive(False)
        finish_label = self.builder.get_object("finish_label")
        if completed:
            finish_label.set_text("Message successfully sent")
        else:
            finish_label.set_text("Error sending the message")

    def on_finish_send_clicked(self, button):
        # Returns to the starting panel 1
        sp1 = self.builder.get_object("send_panel_1")
        sp1.show()
        sp2 = self.builder.get_object("send_panel_2")
        sp2.hide()
        finish_button = self.builder.get_object("finish_send_button")
        finish_button.set_sensitive(False)
        stop_button = self.builder.get_object("stop_send_button")
        stop_button.set_sensitive(True)
        self.notebook.set_current_page(0)

    def on_start_receive_clicked(self, button):
        logging.info("start receiving")
        stop_button = self.builder.get_object("stop_receive_button")
        stop_button.set_sensitive(True)
        button.set_sensitive(False)
        received_text_view = self.builder.get_object("code_generated_text_view")
        received_text_view.get_buffer().set_text("")
        received_text_view = self.builder.get_object("received_text_view")
        received_text_view.get_buffer().set_text("")

        worm.start_receive(self.on_code_generated, self.on_message_received)

    def on_code_generated(self, code):
        received_text_view = self.builder.get_object("code_generated_text_view")
        received_text_view.get_buffer().set_text(code)

    def on_message_received(self, message):
        received_text_view = self.builder.get_object("received_text_view")
        received_text_view.get_buffer().set_text(message.decode("utf-8"))
        stop_button = self.builder.get_object("stop_receive_button")
        stop_button.set_sensitive(False)
        stop_button = self.builder.get_object("start_receive_button")
        stop_button.set_sensitive(True)

    def on_stop_receive_clicked(self, button):
        worm.stop_receiving(self.on_stop_receive_callback)

    def on_stop_receive_callback(self):
        stop_button = self.builder.get_object("stop_receive_button")
        stop_button.set_sensitive(False)
        stop_button = self.builder.get_object("start_receive_button")
        stop_button.set_sensitive(True)


GUI()
Gtk.main()



