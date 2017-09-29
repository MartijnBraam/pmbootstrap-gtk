import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pmbootstrap_gtk.devices import get_devices


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data


selected_device = None


class Handler:
    def onCancelWizard(self, *args):
        Gtk.main_quit(*args)

    def onCloseWizard(self, *args):
        Gtk.main_quit(*args)

    def onApply(self, button):
        print("Hello World!")

    def onRefreshDevices(self, button):
        print("refreshing devices...")
        # TODO: do this async
        devices = get_devices()
        listbox_devices = builder.get_object("listbox-devices")

        # Clear current device list
        # for child in listbox_devices.children:
        #    listbox_devices.remove(child)

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

    def set_page_complete(self, page):
        page = builder.get_object(page)
        window.set_page_complete(page, True)

    def onSelectDevice(self, widget, row):
        global selected_device
        selected_device = row.data
        print("Selected {}.".format(selected_device["name"]))
        self.set_page_complete("introductionbox")


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("wizard.glade")
    builder.connect_signals(Handler())
    window = builder.get_object("assistant1")
    window.show_all()
    Gtk.main()
