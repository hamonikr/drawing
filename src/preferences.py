# preferences.py
#
# Copyright 2018-2021 Romain F. T.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gio, Gdk
from .utilities import utilities_add_unit_to_spinbtn

@Gtk.Template(resource_path='/com/github/maoschanz/drawing/ui/preferences.ui')
class DrPrefsWindow(Gtk.Window):
	__gtype_name__ = 'DrPrefsWindow'

	content_area = Gtk.Template.Child()
	stack = Gtk.Template.Child()

	page_images = Gtk.Template.Child()
	page_tools = Gtk.Template.Child()
	page_advanced = Gtk.Template.Child()

	adj_width = Gtk.Template.Child()
	adj_height = Gtk.Template.Child()
	adj_preview = Gtk.Template.Child()

	_current_grid = None
	_grid_attach_cpt = 0
	_gsettings = Gio.Settings.new('com.github.maoschanz.drawing')

	def __init__(self, is_beta, wants_csd, **kwargs):
		super().__init__(**kwargs)
		if wants_csd:
			header_bar = Gtk.HeaderBar(
				visible=True, \
				title=_("Preferences"), \
				show_close_button=True \
			)
			self.set_titlebar(header_bar)
			stack_switcher = Gtk.StackSwitcher(
				visible=True, \
				stack=self.stack, \
				halign=Gtk.Align.CENTER \
			)
			header_bar.set_custom_title(stack_switcher)
			self.set_default_size(480, 500)
		else:
			stack_sidebar = Gtk.StackSidebar(visible=True, stack=self.stack)
			stack_sidebar.set_size_request(140, -1)
			self.content_area.pack_start(stack_sidebar, False, False, 0)
			self.set_default_size(600, 400) # Not high enough but the golden
			# ratio is more important than usability

		if is_beta:
			self.get_style_context().add_class('devel')

		self.page_builder_images()
		self.page_builder_tools()
		self.page_builder_advanced(is_beta)

	# Each `page_*` attribute is a GtkGrid. Each `page_builder_*` method declare
	# its grid to be the currently filled one, and reset the counter.
	# Then, each `page_builder_*` method will call the `add_*` methods, who will
	# build accurate widgets to be packed on the grid by the `attach_*` methods.

	############################################################################

	def set_current_grid(self, grid):
		self._current_grid = grid
		self._grid_attach_cpt = 0

	def update_grid_cpt(self):
		self._grid_attach_cpt = self._grid_attach_cpt + 1

	############################################################################

	def page_builder_images(self):
		"""Adds the widget to the grid of the 'images' page."""
		self.set_current_grid(self.page_images)

		# Context: title of a section of the preferences
		self.add_section_title(_("New images"))
		self.add_adj(_("Default width"), 'default-width', self.adj_width)
		self.add_adj(_("Default height"), 'default-height', self.adj_height)
		self.add_colorbtn(_("Default color"), 'default-rgba')

		self.add_section_separator()
		# Context: title of a section of the preferences
		self.add_section_title(_("Images saving"))
		self.add_help(_("JPEG and BMP images can't handle transparency.") + \
		        " " + _("If you save your images in these formats, what " + \
		                  "do want to use to replace transparent pixels?"))
		alpha_dict = {
			# Context: this is the label that describes the initial color of an
			# image (as set in the preferences or in the "new image with custom
			# size" dialog). This is displayed in the context of editing or
			# saving the image, but not when creating it.
			'initial': _("Default color"),
			'white': _("White"),
			'black': _("Black"),
			# Context: replace transparent pixels with [checkboard]. This is a
			# pattern of dark and light greys.
			'checkboard': _("Checkboard"),
			# Context: replace transparent pixels with [nothing]. In practice it
			# means the alpha channel is just removed.
			'nothing': _("Nothing"),
			'ask': _("Ask before saving")
		}
		self.add_radio_flowbox('replace-alpha', alpha_dict)

		self.add_section_separator()
		self.add_section_title(_("Zoom"))
		zoom_help = _("You can zoom with Ctrl+scrolling, or only scrolling.") + \
		                   " " + _("See the user help manual for explanations.")
		self.add_help(zoom_help)
		self.add_switch(_("Use 'Ctrl' to zoom"), 'ctrl-zoom')

	def page_builder_tools(self):
		"""Adds the widget to the grid of the 'tools' page."""
		self.set_current_grid(self.page_tools)

		# Context: title of a section of the preferences (appearance of the
		# tools: big icons?, labels?)
		self.add_section_title(_("Appearance"))
		self.add_switch(_("Show tools names"), 'show-labels')
		self.add_switch(_("Use big icons"), 'big-icons')

		self.add_section_separator()
		# Context: title of a section of the preferences
		self.add_section_title(_("Additional tools"))
		self.add_help(_("These tools are not as reliable and useful as " + \
		       "they should be, so they are not all enabled by default."))
		tools_dict = {
			'eraser': _("Eraser"),
			'highlight': _("Highlighter"),
			'brush': _("Brush"),
			'points': _("Points"),
			'free_select': _("Free selection"),
			'color_select': _("Color selection"),
			'picker': _("Color Picker"),
			'paint': _("Paint")
		}
		self.add_check_flowbox('disabled-tools', tools_dict)

	def page_builder_advanced(self, is_beta):
		"""Adds the widget to the grid of the 'advanced' page."""
		self.set_current_grid(self.page_advanced)

		# Context: title of a section of the preferences
		self.add_section_title(_("Advanced options"))
		self.add_adj(_("Preview size"), 'preview-size', self.adj_preview)
		if is_beta:
			# This label will not be displayed in the UI of stable versions
			self.add_switch(_("Development features"), 'devel-only')
		else:
			self._gsettings.set_boolean('devel-only', False)
		self.add_colorbtn(_("Background color"), 'ui-background-rgba')

		self.add_section_separator()
		
		self.add_section_title(_("Theme variant"))
		variants_dict = {
			'default': _("Default variant"),
			'light': _("Light variant"),
			'dark': _("Dark variant")
		}
		self.add_radio_flowbox('theme-variant', variants_dict)

		self.add_section_separator()
		# Context: title of a section of the preferences. It corresponds to the
		# window layout (header-bar? tool-bar? menu-bar?)
		self.add_section_title(_("Layout"))
		self.add_help(_("The recommended value is \"Automatic\"."))
		# h = headerbar; g = gnome; e = elementary
		# m = menubar; t = toolbar
		# c = color; s = symbolic
		layouts_dict = {
			# It has to match what's written in the previous string.
			'': _("Automatic"),
			'hg': _("Compact"),
			'he': _("elementary OS"),
			# "Legacy" is about the window layout, it means menubar+toolbar, you
			# can translate it like if it was "Traditional"
			'mtc': _("Legacy"),
			# "Legacy" is about the window layout, it means menubar+toolbar, you
			# can translate it like if it was "Traditional".
			# Symbolic icons are monochrome icons.
			'mts': _("Legacy (symbolic icons)"),
			'm': _("Menubar only"),
			'tc': _("Toolbar only"),
			# Symbolic icons are monochrome icons.
			'ts': _("Toolbar only (symbolic icons)")
		}
		self.add_radio_flowbox('deco-type', layouts_dict)

	############################################################################
	# Generic methods to build and pack widgets ################################

	def add_section_separator(self):
		self.attach_large(Gtk.Separator())

	def add_section_title(self, label_text):
		label = Gtk.Label(halign=Gtk.Align.START, use_markup=True, \
		                                    label=('<b>' + label_text + '</b>'))
		self.attach_large(label)

	def add_help(self, label_text):
		help_btn = Gtk.Button.new_from_icon_name('help-faq-symbolic', \
		                                                    Gtk.IconSize.BUTTON)
		help_btn.set_valign(Gtk.Align.CENTER)
		help_btn.set_relief(Gtk.ReliefStyle.NONE)
		help_btn.set_action_name('app.help_prefs') # could be a parameter

		label = Gtk.Label(label=label_text)
		label.set_line_wrap(True)
		label.get_style_context().add_class('dim-label')

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		box.pack_start(label, expand=False, fill=False, padding=0)
		box.pack_end(help_btn, expand=False, fill=False, padding=0)
		box.show_all()
		self.attach_large(box)

	def add_row(self, label_text, widget):
		label = Gtk.Label(label=label_text)
		self.attach_two(label, widget)

	def add_switch(self, label_text, key):
		switch = Gtk.Switch()
		switch.set_active(self._gsettings.get_boolean(key))
		switch.connect('notify::active', self.on_bool_changed, key)
		self.add_row(label_text, switch)

	def add_colorbtn(self, label_text, key):
		color_btn = Gtk.ColorButton(use_alpha=True)
		background_rgba = self._gsettings.get_strv(key)
		r = float(background_rgba[0])
		g = float(background_rgba[1])
		b = float(background_rgba[2])
		a = float(background_rgba[3])
		color = Gdk.RGBA(red=r, green=g, blue=b, alpha=a)
		color_btn.set_rgba(color)
		color_btn.connect('color-set', self.on_colorbtn_changed, key)
		self.add_row(label_text, color_btn)

	def add_adj(self, label_text, key, adj):
		spinbtn = Gtk.SpinButton(adjustment=adj)
		spinbtn.set_value(self._gsettings.get_int(key))
		utilities_add_unit_to_spinbtn(spinbtn, 4, 'px')
		spinbtn.connect('value-changed', self.on_adj_changed, key)
		self.add_row(label_text, spinbtn)

	def add_radio_flowbox(self, setting_key, labels_dict):
		flowbox = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, expand=True)
		self._radio_are_active = False
		w0 = None
		for id0 in labels_dict:
			w0 = self.build_radio_btn(labels_dict[id0], id0, setting_key, w0)
			flowbox.add(w0)
		self._radio_are_active = True
		self.attach_large(flowbox)

	def build_radio_btn(self, label, btn_id, key, group):
		btn = Gtk.RadioButton(label=label, visible=True, group=group)
		active_id = self._gsettings.get_string(key)
		btn.set_active(btn_id == active_id)
		btn.connect('toggled', self.on_radio_btn_changed, key, btn_id)
		return btn

	def add_check_flowbox(self, setting_key, labels_dict):
		flowbox = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, expand=True)
		for id0 in labels_dict:
			w0 = self.build_check_btn(labels_dict[id0], id0, setting_key)
			flowbox.add(w0)
		self.attach_large(flowbox)

	def build_check_btn(self, label, row_id, key):
		btn = Gtk.CheckButton(label=label, visible=True)
		array_of_strings = self._gsettings.get_strv(key)
		btn.set_active(row_id not in array_of_strings)
		btn.connect('toggled', self.on_check_btn_changed, key, row_id)
		return btn

	############################################################################
	# Generic callbacks ########################################################

	def on_bool_changed(self, switch, state, key):
		self._gsettings.set_boolean(key, switch.get_active())

	def on_adj_changed(self, spinbtn, key):
		self._gsettings.set_int(key, spinbtn.get_value_as_int())

	def on_check_btn_changed(self, checkbtn, key, btn_id):
		array_of_strings = self._gsettings.get_strv(key)
		if checkbtn.get_active():
			array_of_strings.remove(btn_id)
		else:
			array_of_strings.append(btn_id)
		self._gsettings.set_strv(key, array_of_strings)

	def on_radio_btn_changed(self, radiobtn, key, btn_id):
		if self._radio_are_active:
			self._gsettings.set_string(key, btn_id)

	def on_colorbtn_changed(self, color_btn, key):
		c = color_btn.get_rgba()
		color_array = [str(c.red), str(c.green), str(c.blue), str(c.alpha)]
		self._gsettings.set_strv(key, color_array)

	############################################################################
	# Low-level packing ########################################################

	def attach_two(self, widget1, widget2):
		widget1.set_halign(Gtk.Align.END)
		widget2.set_halign(Gtk.Align.START)
		widget1.set_visible(True)
		widget2.set_visible(True)
		self._current_grid.attach(widget1, 0, self._grid_attach_cpt, 1, 1)
		self._current_grid.attach(widget2, 1, self._grid_attach_cpt, 1, 1)
		self.update_grid_cpt()

	def attach_large(self, widget):
		widget.set_visible(True)
		self._current_grid.attach(widget, 0, self._grid_attach_cpt, 2, 1)
		self.update_grid_cpt()

	############################################################################
################################################################################

