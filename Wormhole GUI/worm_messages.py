import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
import logging

# All reactor parts should be checked for correctness
from twisted.internet import gtk3reactor
gtk3reactor.install()

from twisted.internet import reactor
import wormhole_functions as worm

logger = logging.getLogger(__name__)

class GUI:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('window.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("appwindow")
        self.window.show()
        text_buffer = self.builder.get_object("receive_code").get_buffer()
        text_buffer.connect('changed', self.on_code_text_changed)

        reactor.run()

    @staticmethod
    def on_delete_window(*args):
        reactor.callFromThread(reactor.stop)
        Gtk.main_quit(*args)

    def on_code_text_changed(self, entryObject, *args):
        receive_button = self.builder.get_object("receive_button")
        # Check if the code field is not empty
        if len(entryObject.get_text(*entryObject.get_bounds(), False)) > 0:
            receive_button.set_sensitive(True)
        else:
            receive_button.set_sensitive(False)

    def on_send_button_clicked(self, button):
        text_buffer = self.builder.get_object("text_to_send").get_buffer()
        message = text_buffer.get_text(*text_buffer.get_bounds(), False)
        if message == "":
            message = "Hello World :)"

        next_page = "send_panel_2"
        stack = self.builder.get_object("send_stack")
        code_label = self.builder.get_object("code_label")
        code_label.set_label("code:")
        wormhole_label = self.builder.get_object("wormhole_code")
        wormhole_label.set_label("")
        finish_button = self.builder.get_object("finish_button_1")
        finish_button.set_sensitive(False)
        back_button = self.builder.get_object("back_button")
        back_button.set_sensitive(True)
        stack.set_visible_child_name(next_page)

        worm.send(message, self.on_code_generated, self.on_message_callback)

    def on_stop_send_clicked(self, button):
        worm.stop_sending(self.on_stop_send_callback)

    def on_stop_send_callback(self):
        self.on_finish_button_1_clicked(None)

    def on_message_callback(self, completed):
        code_label = self.builder.get_object("code_label")
        code_label.set_label("")
        result_label = self.builder.get_object("wormhole_code")
        finish_button = self.builder.get_object("finish_button_1")
        finish_button.set_sensitive(True)
        if completed:
            result_label.set_text("Message successfully sent")
        else:
            result_label.set_text("Error sending the message")

    def on_finish_button_1_clicked(self, button):
        next_page = "send_panel_1"
        text_to_send = self.builder.get_object("text_to_send")
        text_to_send.get_buffer().set_text("")
        back_button = self.builder.get_object("back_button")
        back_button.set_sensitive(False)
        stack = self.builder.get_object("send_stack")
        stack.set_visible_child_name(next_page)

    def on_receive_button_clicked(self, button):
        logging.info("start receiving")
        text_buffer = self.builder.get_object("receive_code").get_buffer()

        # text_buffer.get_bounds() means "get the entire message"
        code = text_buffer.get_text(*text_buffer.get_bounds(), False)
        next_page = "receive_panel_2"
        stack = self.builder.get_object("receive_stack")
        status_label = self.builder.get_object("receive_status")
        status_label.set_label("Trying to download, please wait...")
        finish_button = self.builder.get_object("finish_button_2")
        finish_button.set_sensitive(False)
        back_button = self.builder.get_object("back_button")
        back_button.set_sensitive(True)
        stack.set_visible_child_name(next_page)

        worm.start_receive(code, self.on_message_received)

    def on_code_generated(self, code):
        wormhole_code = self.builder.get_object("wormhole_code")
        wormhole_code.set_label(code)

    def on_message_received(self, message):
        status_label = self.builder.get_object("receive_status")
        status_label.set_label("Message received:")
        received_text = self.builder.get_object("received_text")
        received_text.set_label(message.decode("utf-8"))
        finish_button = self.builder.get_object("finish_button_2")
        finish_button.set_sensitive(True)

    def on_finish_button_2_clicked(self, button):
        next_page = "receive_panel_1"
        receive_code = self.builder.get_object("receive_code")
        receive_code.get_buffer().set_text("")
        back_button = self.builder.get_object("back_button")
        back_button.set_sensitive(False)
        stack = self.builder.get_object("receive_stack")
        stack.set_visible_child_name(next_page)

    def on_stop_receive_clicked(self, button):
        worm.stop_receiving(self.on_stop_receive_callback)

    def on_stop_receive_callback(self):
        self.on_finish_button_2_clicked(None)

    def on_back_button_clicked(self, button):
        stack = self.builder.get_object("send_receive_stack")
        visible = stack.get_visible_child_name()
        if visible == "receive_stack":
            worm.stop_receiving(self.on_stop_receive_callback)
        elif visible == "send_stack":
            worm.stop_sending(self.on_stop_send_callback)


GUI()
Gtk.main()



