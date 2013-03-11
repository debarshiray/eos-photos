from gi.repository import Gtk
from widgets.list_button import ListButton
from widgets.adjust_widget import AdjustWidget
import random

from widgets.list_icon import IconList


class PhotosLeftToolbar(Gtk.VBox):
    """
    The left filter selection toolbar for the photo app.
    """
    def __init__(self, images_path="", **kw):
        super(PhotosLeftToolbar, self).__init__(homogeneous=False, spacing=0, **kw)
        self._images_path = images_path

        self._categories = {}

        self._filter_icons = IconList()
        filter_align = Gtk.Alignment(xalign=0.0, yalign=0.0, xscale=0.0, yscale=0.0, left_padding=30)
        filter_align.add(self._filter_icons)
        self._categories["filters"] = Category(filter_align,
            images_path=self._images_path, label_name=_("FILTERS"),
            expanded_callback=lambda: self.change_category("filters"))

        border_icons = IconList()
        border_align = Gtk.Alignment(xalign=0.0, yalign=0.0, xscale=0.0, yscale=0.0, left_padding=0)
        border_align.add(border_icons)
        self._categories["borders"] = Category(border_align,
            images_path=self._images_path, label_name=_("BORDERS"),
            expanded_callback=lambda: self.change_category("borders"))


        adjustments = AdjustWidget(change_callback=lambda adj_type, value: self._presenter.change_adjusts(adj_type, value))
        adjustments_align = Gtk.Alignment(xalign=0.0, yalign=0.0, xscale=1.0, yscale=0.0, left_padding=15)
        adjustments_align.add(adjustments)
        self._categories["adjustments"] = Category(adjustments_align, 
            images_path=self._images_path, label_name=_("ADJUSTMENTS"),
            expanded_callback=lambda: self.change_category("adjustments"))

        # self._categories["text"] = Category(
        #     images_path=self._images_path, label_name=_("TEXT"), category_name="text",
        #     expanded_callback=lambda: self.change_category("text"))

        # self._categories["transforms"] = Category(
        #     images_path=self._images_path, label_name=_("TRANSFORMS"), category_name="transforms",
        #     expanded_callback=lambda: self.change_category("transforms"))

        for category in self._categories.values():
            self.pack_start(category, expand=False, fill=True, padding=20)

        self.show_all()

    def set_filters(self, filters, default):
        map(self._add_filter_option, filters)
        self.select_filter(default)

    def _add_filter_option(self, name_and_thumb):
        filter_name = name_and_thumb[0]
        thumbnail_path = self._images_path + "filter_thumbnails/" + name_and_thumb[1]
        self._filter_icons.add_icon(thumbnail_path, "filter", filter_name, lambda: self._presenter.on_filter_select(filter_name))
        self._filter_icons.show_all()

    def select_filter(self, filter_name):
        self._filter_icons.select_icon(filter_name)

    def set_presenter(self, presenter):
        self._presenter = presenter

    def change_category(self, category_name):
        for name, category in self._categories.items():
            if not name == category_name:
                category.deselect()


class Category(Gtk.Expander):
    def __init__(self, widget, images_path="", label_name="", expanded_callback=None, **kw):
        super(Category, self).__init__(**kw)

        self._expanded_callback = expanded_callback
        self._images_path = images_path
        self._title_image = Gtk.Image.new_from_file(images_path + "Filter-icon.png")
        self._title_label = Gtk.Label(label=label_name, name="filters-title")
        self._title_box = Gtk.HBox(homogeneous=False, spacing=0)
        self._title_box.pack_start(self._title_image, expand=False, fill=False, padding=0)
        self._title_box.pack_start(self._title_label, expand=False, fill=False, padding=2)
        self.set_label_widget(self._title_box)
        #self._title_allign = Gtk.HBox(homogeneous=False, spacing=0)
        #self._title_allign.pack_start(borders_title_box, expand=False, fill=False, padding=10)

        self._widget = widget
        #self._scroll_contents = Gtk.VBox(homogeneous=False, spacing=8)
        self._scroll_area = Gtk.ScrolledWindow(name="filters-scroll-area")
        self._scroll_area.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._scroll_area.add_with_viewport(self._widget)
        self._scroll_area.set_vexpand(True)


        # self._separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        # self.add(self._separator)

        # self._drop_shadow = Gtk.Image.new_from_file(images_path + "Filter-mask-shadow.png")
        # self._drop_shadow.set_halign(Gtk.Align.CENTER)
        # self._drop_shadow.set_valign(Gtk.Align.START)
        # self._overlay = Gtk.Overlay()
        # self._overlay.add(self._scroll_area)
        # self._overlay.add_overlay(self._drop_shadow)

        self.connect('notify::expanded', self.expanded_cb)
        self.set_resize_toplevel(True)

    def expanded_cb(self, widget, event):
        if self.get_expanded():
            # self._title_box.select()
            self.add(self._scroll_area)
            self._expanded_callback()
        else:
            self.remove(self._scroll_area)
            # self._title_box.deselect()
        self.show_all()


    def get_widget(self):
        return self._widget

    def select(self):
        self.set_expanded(True)

    def deselect(self):
        self.set_expanded(False)

    def is_selected(self):
        return self.get_expanded()

    # def add_to_scroll(self, object_):
    #     align = Gtk.HBox(homogeneous=False, spacing=0)
    #     align.pack_start(object_, expand=False, fill=False, padding=30)
    #     self._scroll_contents.pack_start(align, expand=False, fill=False, padding=0)
    #     self.show_all()
