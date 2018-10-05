import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pmbootstrap_gtk
from pmbootstrap_gtk.devices import get_devices
from pmbootstrap_gtk.pmb_interface import list_supported_devices


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data


selected_device = None
selected_port = None
initialized = False


class Handler:
    def on_wizard_prepare(self, *args):
        global initialized
        if initialized:
            return
        initialized = True
        print("Preparing device information")
        devices = list_supported_devices()
        listbox_devices = builder.get_object("listbox-supported-devices")
        for device in devices:
            row = ListBoxRowWithData(device)
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            pixbuf = Gtk.IconTheme.get_default().load_icon("phone", 64, 0)
            device_name = Gtk.Label(device, xalign=0)
            device_name.set_markup("<b>{}</b>".format(device))
            vbox.pack_start(device_name, True, True, 0)
            icon = Gtk.Image.new_from_pixbuf(pixbuf)
            alignment1 = Gtk.Alignment()
            alignment1.add(icon)
            alignment1.set(-1, 0, 0, 0)
            hbox.pack_start(alignment1, True, True, 0)
            alignment2 = Gtk.Alignment()
            alignment2.add(vbox)
            alignment2.set(-1, 0, 0, 0)
            hbox.pack_start(alignment2, True, True, 0)
            row.add(hbox)
            listbox_devices.add(row)
        listbox_devices.show_all()
        self.on_refresh_devices(args[0])

    def on_cancel_wizard(self, *args):
        Gtk.main_quit(*args)

    def on_close_wizard(self, *args):
        Gtk.main_quit(*args)

    def on_apply(self, button):
        print("Hello World!")

    def on_refresh_devices(self, button):
        print("refreshing devices...")
        # TODO: do this async
        devices = get_devices()
        listbox_devices = builder.get_object("listbox-devices")

        # Clear current device list
        # for child in listbox_devices.children:
        #     listbox_devices.remove(child)

        # Build new listbox items for the devices
        for device in devices:
            row = ListBoxRowWithData(device)
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            if device["type"] == "adb":
                pixbuf = Gtk.IconTheme.get_default().load_icon("phone", 64, 0)
                device_name = Gtk.Label(device["name"], xalign=0)
                device_name.set_markup("<b>{}</b>".format(device["name"]))
                vbox.pack_start(device_name, True, True, 0)
                device_detail = Gtk.Label(device["serial"], xalign=0)
                vbox.pack_start(device_detail, True, True, 0)
            elif device["type"] == "sdcard":
                pixbuf = Gtk.IconTheme.get_default().load_icon("drive-removable-media", 64, 0)
                device_name = Gtk.Label(device["name"], xalign=0)
                device_name.set_markup("<b>{}</b>".format(device["name"]))
                vbox.pack_start(device_name, True, True, 0)
                device_detail = Gtk.Label("Size: {}".format(device["size"]), xalign=0)
                vbox.pack_start(device_detail, True, True, 0)
            icon = Gtk.Image.new_from_pixbuf(pixbuf)
            alignment1 = Gtk.Alignment()
            alignment1.add(icon)
            alignment1.set(-1, 0, 0, 0)
            hbox.pack_start(alignment1, True, True, 0)
            alignment2 = Gtk.Alignment()
            alignment2.add(vbox)
            alignment2.set(-1, 0, 0, 0)
            hbox.pack_start(alignment2, True, True, 0)
            row.add(hbox)
            listbox_devices.add(row)
        listbox_devices.show_all()

    def set_page_complete(self, page, state=True):
        page = builder.get_object(page)
        window.set_page_complete(page, state)

    def on_select_device(self, widget, row):
        global selected_device
        selected_device = row.data
        print("Selected {}.".format(selected_device["name"]))
        self.set_page_complete("introductionbox")

    def on_select_supported_device(self, widget, row):
        global selected_port
        selected_port = row.data
        print("Selected {}.".format(selected_port))
        self.set_page_complete("deviceselectionbox")

    def on_fde_password_changed(self, textbox):
        if len(textbox.get_text()) == 0:
            self.set_page_complete("encryptionbox", False)
        else:
            self.set_page_complete("encryptionbox")

    def on_enable_disable_fde(self, checkbox):
        fde_password_entry = builder.get_object("fde-password")
        if checkbox.get_active():
            fde_password_entry.set_editable(True)
            if len(fde_password_entry.get_text()) == 0:
                self.set_page_complete("encryptionbox", False)
            else:
                self.set_page_complete("encryptionbox")
            print("FDE Enabled")
        else:
            fde_password_entry.set_editable(False)
            print("FDE Disabled")
            self.set_page_complete("encryptionbox")

    def on_userinfo_changed(self, textbox):
        boxes = ["username", "password", "hostname"]
        complete = True
        for box in boxes:
            widget = builder.get_object(box)
            if widget.get_text() == "":
                complete = False
                break

        if complete:
            self.set_page_complete("userinfobox")
        else:
            self.set_page_complete("userinfobox", True)


if __name__ == '__main__':
    import os

    moduledir = os.path.dirname(pmbootstrap_gtk.__file__)
    builder = Gtk.Builder()
    builder.add_from_file(os.path.join(moduledir, "wizard.glade"))
    builder.connect_signals(Handler())
    window = builder.get_object("assistant1")
    window.show_all()
    Gtk.main()
