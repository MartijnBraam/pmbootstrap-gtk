import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

import pmbootstrap_gtk
from pmbootstrap_gtk.devices import get_devices
from pmbootstrap_gtk.uis import get_uis


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data


selected_device = None


class Handler:
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
            alignment1 = Gtk.Alignment(margin=15)
            alignment1.add(icon)
            alignment1.set(-1, 0, 0, 0)
            hbox.pack_start(alignment1, False, False, 0)
            alignment2 = Gtk.Alignment(margin=15)
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
            self.populate_uis() # should not be here obviously
            self.set_page_complete("userinfobox", True)
            
    def populate_uis(self):
        uis = get_uis()
        store = Gtk.ListStore(str, str, str)
        
        gui_list = builder.get_object("gui-list")
        
        renderer = Gtk.CellRendererText(wrap_width = 400, wrap_mode = Pango.WrapMode.WORD)
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        gui_list.append_column(column)

        column = Gtk.TreeViewColumn("Type", renderer, text=1)
        gui_list.append_column(column)
        
        column = Gtk.TreeViewColumn("Description", renderer, text=2)
        gui_list.append_column(column)
        
        
        # Build new listbox items for the devices
        for ui in uis:
            store.append([ui['name'], ui['type'], ui['description']])
        
        for row in store:
            # Print values of all columns
            print(row[:])
        gui_list.set_model(store)
        gui_list.show_all()
        
    def on_ui_chosen(self, tree, ui, x):
        # update thumbnail
        
        self.set_page_complete("guibox")


if __name__ == '__main__':
    import os
    moduledir = os.path.dirname(pmbootstrap_gtk.__file__)
    builder = Gtk.Builder()
    builder.add_from_file(os.path.join(moduledir, "wizard.glade"))
    builder.connect_signals(Handler())
    window = builder.get_object("assistant1")
    window.show_all()
    Gtk.main()
