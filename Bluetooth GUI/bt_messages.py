import gi
import bluetooth_pybluez as pybluez
import logging
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

        # Initialize the treeview
        bluetooth_tree_view = self.builder.get_object("bluetooth_tree_view")
        cell0 = Gtk.CellRendererText()
        col0 = Gtk.TreeViewColumn("name", cell0, text=0)
        bluetooth_tree_view.append_column(col0)
        col1 = Gtk.TreeViewColumn("mac", cell0, text=1)
        bluetooth_tree_view.append_column(col1)

        self.notebook = self.builder.get_object("notebook")
        sp2 = self.builder.get_object("send_panel_2")
        sp3 = self.builder.get_object("send_panel_3")
        self.notebook.prepend_page(sp2, Gtk.Label("Send"))
        self.notebook.prepend_page(sp3, Gtk.Label("Send"))
        sp2.hide()
        sp3.hide()

    @staticmethod
    def on_delete_window(*args):
        Gtk.main_quit(*args)

    def on_send_pressed(self, button):
        # Hide the panel 1 and display the panel 2
        sp2 = self.builder.get_object("send_panel_2")
        sp2.show()
        self.notebook.set_current_page(1)
        sp1 = self.builder.get_object("send_panel_1")
        sp1.hide()

        pybluez.discover(self.discover_ends)

    def discover_ends(self, devices_found):
        logger.info("discovery ended")
        bl = self.builder.get_object("bluetooth_list")
        bl.clear()
        choose_button = self.builder.get_object("choose_button_1")

        # Until the user select a receiver, the choose button is not sensitive
        choose_button.set_sensitive(False)
        if len(devices_found) > 0:
            for address, name in devices_found:
                bl.append([name, address])
        else:
            bl.append(["No devices found", ""])

    def on_row_activated(self, tree_view, path, column):
        bluetooth_tree_view = self.builder.get_object("bluetooth_tree_view")
        tree_selection = bluetooth_tree_view.get_selection()
        (model, iterator) = tree_selection.get_selected()
        mac = model.get(iterator, 1)[0]
        choose_button = self.builder.get_object("choose_button_1")

        # Check if the selected row is valid
        choose_button.set_sensitive(mac != "")

    def on_back_clicked(self, button):
        # Hide the panel 2 and display the panel 1
        sp1 = self.builder.get_object("send_panel_1")
        sp1.show()
        sp2 = self.builder.get_object("send_panel_2")
        sp2.hide()
        self.notebook.set_current_page(0)

    def on_choose_clicked(self, button):
        bluetooth_tree_view = self.builder.get_object("bluetooth_tree_view")
        tree_selection = bluetooth_tree_view.get_selection()
        (model, iterator) = tree_selection.get_selected()
        mac = model.get(iterator, 1)[0]
        text_buffer = self.builder.get_object("text_to_send").get_buffer()

        # text_buffer.get_bounds() means "get the entire message"
        message = text_buffer.get_text(*text_buffer.get_bounds(), False)
        if message == "":
            message = "Hello World :)"

        finish_label = self.builder.get_object("finish_label")
        finish_label.set_text("Sending the message")
        sp3 = self.builder.get_object("send_panel_3")
        sp3.show()
        sp2 = self.builder.get_object("send_panel_2")
        sp2.hide()
        self.notebook.set_current_page(0)

        pybluez.send(mac, 3, message, self.on_message_callback)

    def on_message_callback(self, completed):
        finish_label = self.builder.get_object("finish_label")
        if completed:
            finish_label.set_text("Message successfully sent")
        else:
            finish_label.set_text("Error sending the message")

    def on_finish_clicked(self, button):
        # Returns to the starting panel 1
        sp1 = self.builder.get_object("send_panel_1")
        sp1.show()
        sp3 = self.builder.get_object("send_panel_3")
        sp3.hide()
        self.notebook.set_current_page(0)

    def on_start_clicked(self, button):
        print("start")
        stop_button = self.builder.get_object("stop_button")
        stop_button.set_sensitive(True)
        button.set_sensitive(False)

        pybluez.start_receive(3, 1024, self.server_data_received)

    def on_stop_clicked(self, button):
        print("stop")
        start_button = self.builder.get_object("start_button")
        start_button.set_sensitive(True)
        button.set_sensitive(False)
        pybluez.stop_receive()

    def server_data_received(self, received_text):
        received_text_view = self.builder.get_object("received_text_view")
        received_text_view.get_buffer().set_text(received_text.decode("utf-8"))
        start_button = self.builder.get_object("start_button")
        start_button.set_sensitive(True)
        stop_button = self.builder.get_object("stop_button")
        stop_button.set_sensitive(False)


GUI()
Gtk.main()



