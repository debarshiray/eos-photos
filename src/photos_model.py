import collections

import Image
import ImageFilter

import image_processing.image_tools as ImageTools
from photos_image_widget import PhotosImageWidget


class PhotosModel(object):
    """
    The model for the photo being edited. Uses the Python Imaging Library to
    modify the current open photo.
    """
    def __init__(self, textures_path="", curves_path=""):
        super(PhotosModel, self).__init__()
        ImageTools.set_textures_path(textures_path)
        self._textures_path = textures_path
        ImageTools.set_curves_path(curves_path)
        self._curves_path = curves_path
        self._source_image = None
        self._filtered_image = None
	self._blurred_image = None
        self._adjusted_image = None
        self._image_widget = PhotosImageWidget()

        self._is_saved = True
        self._build_filter_dict()
        self._build_border_dict()
	self._build_blur_dict()
        self._clear_options()

    def _build_blur_dict(self):
	self._blur_dict = collections.OrderedDict([
	    (_("NONE"), lambda im: im),
	    (_("TILT-SHIFT"), lambda im: ImageTools.tilt_shift_blur(im)),
	    (_("DEPTH-OF-FIELD"), lambda im: ImageTools.depth_of_field_blur(im))
	])

    def _build_filter_dict(self):
        self._filter_dict = collections.OrderedDict([
            (_("NORMAL"), lambda im: im),
            (_("GRAYSCALE"), lambda im: ImageTools.grayscale(im)),
            (_("COUNTRY"), lambda im: ImageTools.country(im)),
            (_("GRUNGIFY"), lambda im: ImageTools.grunge(im)),
            (_("OLD PHOTO"), lambda im: ImageTools.old_photo(im)),
            (_("COLORFUL"), lambda im: ImageTools.colorful(im)),
            # (_("BUMPY"), lambda im: ImageTools.bumpy(im)),
            (_("LUMO"), lambda im: ImageTools.lumo(im)),
            # (_("SMOOTH"), lambda im: im.filter(ImageFilter.SMOOTH_MORE)),
            # (_("SHARPEN"), lambda im: im.filter(ImageFilter.SHARPEN)),
            (_("FOGGY BLUE"), lambda im: ImageTools.foggy_blue(im)),
            (_("PAPER"), lambda im: ImageTools.paper(im)),
            (_("TRAINS"), lambda im: ImageTools.trains(im)),
            (_("DESERT"), lambda im: ImageTools.desert(im)),
            (_("POSTERIZE"), lambda im: ImageTools.posterize(im)),
            (_("INVERT"), lambda im: ImageTools.invert(im)),
            (_("EMBOSS"), lambda im: im.filter(ImageFilter.EMBOSS)),
            (_("EDGES"), lambda im: im.filter(ImageFilter.FIND_EDGES)),
            (_("PIXELATE"), lambda im: ImageTools.pixelate(im)),
            (_("BOXELATE"), lambda im: ImageTools.boxelate(im)),
        ])

    def _build_border_dict(self):
        self._border_dict = collections.OrderedDict([
            (_("NONE"), None),
            (_("HORIZONTAL BARS"), "horizontal_bars.png"),
            (_("SIDE BARS"), "vertical_bars.png")
        ])

    def _clear_options(self):
        self._filter = self._get_default_filter()
        self._brightness = 1.0
        self._contrast = 1.0
        self._saturation = 1.0
        self._last_filter = ""
	self._last_blur_type = ""
	self._blur_type = "NONE"
        self._last_brightness = self._last_contrast = self._last_saturation = -1
        self._border = self._get_default_border()

    def _get_default_filter(self):
        return self._filter_dict.keys()[0]

    def _get_default_border(self):
        return self._border_dict.keys()[0]

    def get_image_widget(self):
        return self._image_widget

    def open(self, filename):
        self._filename = filename
        self._clear_options()
        self._source_image = ImageTools.limit_size(Image.open(filename), (2056, 2056)).convert('RGB')
        self._update_base_image()
        self._update_border_image()
        self._is_saved = True

    def save(self, filename, format=None, quality=95):
        if self.is_open():
            im = self._composite_final_image()
            if format is not None:
                im.save(filename, format, quality=quality)
            else:
                im.save(filename, quality=quality)
            self._is_saved = True

    def is_open(self):
        return self._source_image is not None

    def is_saved(self):
        return self._is_saved

    def is_modified(self):
        return self._curr_filter is not self.get_defualt_filter_name()

    def get_current_filename(self):
        if not self.is_open():
            return None
        return self._filename

    def get_filter_names(self):
        return self._filter_dict.keys()

    def get_filter_names_and_thumbnails(self):
        names_and_thumbs = []
        filter_no = 0
        for name in self._filter_dict.keys():
            names_and_thumbs.append((name, "filter_" + str(filter_no) + ".jpg"))
            filter_no += 1
        return names_and_thumbs

    def get_border_names_and_thumbnails(self):
        names_and_thumbs = []
        for name in self._border_dict.keys():
            names_and_thumbs.append((name, "Filters_Example-Picture_01.jpg"))
        return names_and_thumbs

    def get_contrast(self):
        return self._contrast

    def set_contrast(self, value):
        self._contrast = value
        self._update_base_image()

    def get_brightness(self):
        return self._brightness

    def set_blur_type(self, value):
	self._blur_type = value
	self._update_base_image()

    def set_brightness(self, value):
        self._brightness = value
        self._update_base_image()

    def get_saturation(self):
        return self._saturation

    def set_saturation(self, value):
        self._saturation = value
        self._update_base_image()

    def get_filter(self):
        return self._filter

    def set_filter(self, filter_name):
        self._filter = filter_name
        self._update_base_image()

    def get_border(self):
        return self._border

    def set_border(self, border_name):
        if (not self.is_open()):
            return
        self._border = border_name
        self._update_border_image()

    def _update_base_image(self):
        if (not self.is_open()):
            return
        filtered = False
        if not self._filter == self._last_filter:
            if self._filter in self._filter_dict:
                filtered = True
                self._last_filter = self._filter
                self._filtered_image = self._filter_dict[self._filter](self._source_image)
            else:
                print "Filter not supported!"
        adjusted = not (self._last_brightness == self._brightness
                        and self._last_contrast == self._contrast
                        and self._last_saturation == self._saturation)
	blurred = False
	if not self._last_blur_type == self._blur_type:
	    if self._blur_type in self._blur_dict:
	        print self._blur_type
    	        blurred = True
    	        self._last_blur_type = self._blur_type
	        self._blurred_image = self._blur_dict[self._blur_type](self._filtered_image)
	    else:
	        print "Blur not supported!"

        if filtered or adjusted or blurred:
            # adjust image
            im = ImageTools.apply_contrast(self._blurred_image, self._contrast)
            im = ImageTools.apply_brightness(im, self._brightness)
            im = ImageTools.apply_saturation(im, self._saturation)
            self._adjusted_image = im
            # update widget
            width, height = self._adjusted_image.size
            self._image_widget.replace_base_image(
                self._adjusted_image.tostring(), width, height)
            self._is_saved = False

    def _update_border_image(self):
        filename = self._border_dict[self._border]
        if filename is not None:
            self._border_image = Image.open(self._textures_path + filename).resize(
                self._source_image.size, Image.BILINEAR)
            width, height = self._border_image.size
            self._image_widget.replace_border_image(
                self._border_image.tostring(), width, height)
        else:
            self._border_image = None
            self._image_widget.hide_border_image()

    def _composite_final_image(self):
        if self._border_image is None:
            return self._adjusted_image
        return Image.composite(self._border_image, self._adjusted_image, self._border_image)
