# deco_manager.py
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

from gi.repository import Gtk

class DrDecoManagerMenubar():
	__gtype_name__ = 'DrDecoManagerMenubar'
	UI_PATH = '/com/github/maoschanz/drawing/ui/'

	def __init__(self, window, use_menubar):
		window.set_show_menubar(use_menubar)
		self._window = window
		self._main_menu_btn = None
		if use_menubar:
			window.set_titlebar(None) # that's an arbitrary restriction

	def remove_from_ui(self):
		return False

	############################################################################

	def set_titles(self, title_label, subtitle_label):
		full_title = _("Drawing") + ' ~ ' + title_label + ' ~ ' + subtitle_label
		self._window.set_title(full_title)

	def toggle_menu(self):
		if self._main_menu_btn is not None:
			self._main_menu_btn.set_active(not self._main_menu_btn.get_active())

	def set_undo_label(self, label):
		pass # TODO update "undo" item in the menubar

	def set_redo_label(self, label):
		pass # TODO update "redo" item in the menubar

	############################################################################
	# Adaptability #############################################################

	def init_adaptability(self):
		pass

	def adapt_to_window_size(self):
		pass

	def set_compact(self, state):
		pass

	############################################################################
################################################################################

class DrDecoManagerHeaderbar(DrDecoManagerMenubar):
	__gtype_name__ = 'DrDecoManagerHeaderbar'

	def __init__(self, is_eos, window):
		super().__init__(window, False)
		self._is_narrow = True # This is reducing the complexity of resizing,
		# but its main goal is to avoid a GTK minor bug where the initial
		# bunch of configure-event signals was sent to soon.

		# Build the window's headerbar. If "is_eos" is true, the headerbar will
		# follow elementaryOS guidelines, else it will follow GNOME guidelines.
		if is_eos:
			resource_path = self.UI_PATH + 'headerbar-eos.ui'
		else:
			resource_path = self.UI_PATH + 'headerbar.ui'
		builder = Gtk.Builder.new_from_resource(resource_path)
		self._widget = builder.get_object('header_bar')
		window.set_titlebar(self._widget)

		# Code differences are kept minimal between the 2 cases: widgets will
		# share similar names in order to both work with the same method
		# updating widgets' visibility when resizing.
		self._save_long = builder.get_object('save_long')
		self._save_short = builder.get_object('save_short')
		self._hidable_widget_1 = builder.get_object('hidable1')
		self._hidable_widget_2 = builder.get_object('hidable2')

		# Mandatory widget name, used for the `win.main_menu` action
		self._main_menu_btn = builder.get_object('main_menu_btn')

		# History buttons whose tooltips depends on the last operation
		self._undo_btn = builder.get_object('undo_btn')
		self._redo_btn = builder.get_object('redo_btn')

		# Quite extreme as a precaution, will be more precise later
		self._limit_size = 750
		self._manual_correction = 0

		builder.add_from_resource(self.UI_PATH + 'win-menus.ui')
		if is_eos:
			self._init_menus_eos(builder)
		else:
			self._init_menus_gnome(builder)

		# The longer one is set by default to be consistent with the initial
		# value of self._is_narrow
		self._main_menu_btn.set_menu_model(self._long_primary_menu)

	def _init_menus_gnome(self, builder):
		"""Sets the menus for the GNOME/Budgie layout: `self._hidable_widget_2`
		is the "New Image" button here."""
		self._short_primary_menu = builder.get_object('short-window-menu')
		self._long_primary_menu = builder.get_object('long-window-menu')
		self._hidable_widget_2.set_menu_model(builder.get_object('new-image-menu'))

	def _init_menus_eos(self, builder):
		"""Sets the menus for the Pantheon layout: the "New Image" button isn't
		hidden here, and menus are shorter."""
		self._short_primary_menu = builder.get_object('minimal-window-menu')
		self._long_primary_menu = builder.get_object('short-window-menu')
		save_as_menubtn = builder.get_object('hidable1')
		save_as_menubtn.set_menu_model(builder.get_object('save-section'))
		share_menubtn = builder.get_object('hidable2')
		share_menubtn.set_menu_model(builder.get_object('share-section'))
		new_btn = builder.get_object('new_btn')
		new_btn.set_menu_model(builder.get_object('new-image-menu'))
		self._manual_correction = -50

	def remove_from_ui(self):
		return self._is_narrow

	############################################################################

	def set_titles(self, title_label, subtitle_label):
		super().set_titles(title_label, subtitle_label)
		self._widget.set_title(title_label)
		self._widget.set_subtitle(subtitle_label)

	def set_undo_label(self, label):
		super().set_undo_label(label)
		if label is None:
			self._undo_btn.set_tooltip_text(_("Undo"))
		else:
			self._undo_btn.set_tooltip_text(_("Undo %s") % label)

	def set_redo_label(self, label):
		super().set_redo_label(label)
		if label is None:
			self._redo_btn.set_tooltip_text(_("Redo"))
		else:
			self._redo_btn.set_tooltip_text(_("Redo %s") % label)

	############################################################################
	# Adaptability #############################################################

	def init_adaptability(self):
		# Header bar width limit
		self._widget.show_all()
		widgets_width = self._hidable_widget_1.get_preferred_width()[0] \
		              + self._hidable_widget_2.get_preferred_width()[0] \
		                     + self._save_long.get_preferred_width()[0] \
		                    - self._save_short.get_preferred_width()[0] \
		                      + self._undo_btn.get_preferred_width()[0] \
		                      + self._redo_btn.get_preferred_width()[0]
		widgets_width = widgets_width + self._manual_correction
		self._limit_size = widgets_width * 2.5 # 100% arbitrary
		# print(self._limit_size)
		self.set_compact(True)
		self.adapt_to_window_size()

	def adapt_to_window_size(self):
		can_expand = (self._widget.get_allocated_width() > self._limit_size)
		incoherent = (can_expand == self._is_narrow)
		if incoherent:
			self.set_compact(not self._is_narrow)

	def set_compact(self, state):
		"""Set the compactness of the headerbar: if the parameter is True, wide
		widgets will be hidden in favor of narrow ones. Else, the opposite."""
		# Instead of a boolean, `state` could be an integer, which would be
		# far more complex to handle, but would allow thinner granularity.
		if state:
			self._main_menu_btn.set_menu_model(self._long_primary_menu)
		else:
			self._main_menu_btn.set_menu_model(self._short_primary_menu)
		self._save_long.set_visible(not state)
		self._save_short.set_visible(state)
		self._hidable_widget_1.set_visible(not state)
		self._hidable_widget_2.set_visible(not state)
		self._is_narrow = state

	############################################################################
################################################################################

class DrDecoManagerToolbar(DrDecoManagerMenubar):
	__gtype_name__ = 'DrDecoManagerToolbar'

	def __init__(self, is_symbolic, with_menubar, window):
		super().__init__(window, with_menubar)
		window.set_titlebar(None) # that's an arbitrary restriction
		if is_symbolic:
			resource_path = self.UI_PATH + 'toolbar-symbolic.ui'
		else:
			resource_path = self.UI_PATH + 'toolbar.ui'
		builder = Gtk.Builder.new_from_resource(resource_path)

		# Composition over inheritance
		self._widget = builder.get_object('toolbar')
		window.toolbar_box.pack_start(self._widget, True, True, 0)
		window.toolbar_box.show_all()

		# Mandatory widget name, used for the `win.main_menu` action
		self._main_menu_btn = builder.get_object('main_menu_btn')

		# History buttons whose tooltips depends on the last operation
		# XXX maybe later
		# self._undo_btn = builder.get_object('undo_btn')
		# self._redo_btn = builder.get_object('redo_btn')

		# The toolbar has menus which need to be set manually
		builder.add_from_resource(self.UI_PATH + 'win-menus.ui')

		new_btn = builder.get_object('new_menu_btn')
		new_menu = Gtk.Menu.new_from_model(builder.get_object('new-image-menu'))
		new_btn.set_menu(new_menu)

		save_btn = builder.get_object('save_menu_btn')
		save_menu = Gtk.Menu.new_from_model(builder.get_object('save-section'))
		save_btn.set_menu(save_menu)

		if with_menubar:
			self._main_menu_btn.set_visible(False)
		else:
			others_menu = builder.get_object('minimal-window-menu')
			self._main_menu_btn.set_menu_model(others_menu)

	def remove_from_ui(self):
		self._widget.destroy()
		return False

	# def set_undo_label(self, label):
	#	super().set_undo_label(label)
	# 	if label is None:
	# 		self._undo_btn.set_tooltip_text(_("Undo"))
	# 	else:
	# 		self._undo_btn.set_tooltip_text(_("Undo %s") % label)

	# def set_redo_label(self, label):
	#	super().set_redo_label(label)
	# 	if label is None:
	# 		self._redo_btn.set_tooltip_text(_("Redo"))
	# 	else:
	# 		self._redo_btn.set_tooltip_text(_("Redo %s") % label)

	############################################################################
################################################################################

