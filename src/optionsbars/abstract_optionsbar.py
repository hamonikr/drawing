# bottombar.py
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

RSRC_PREFIX = '/com/github/maoschanz/drawing/'

class AbstractOptionsBar():
	__gtype_name__ = 'AbstractOptionsBar'
	# Abstract class

	def __init__(self):
		# Quite high as a precaution, will be more precise later
		self._limit_size = 700
		self._is_narrow = False

	def build_ui(self, end_of_path):
		builder = Gtk.Builder.new_from_resource(RSRC_PREFIX + end_of_path)
		self.action_bar = builder.get_object('bottom-pane')
		self.cancel_btn = builder.get_object('cancel_btn') # may be None
		self.centered_box = builder.get_object('centered_box') # may be None
		self.apply_btn = builder.get_object('apply_btn') # may be None
		self.help_btn = builder.get_object('help_btn') # may be None
		return builder # for implementations-specific widgets

	def build_options_menu(self, widget, model, label):
		"""Set a widget (or a menu) as the popover with tools options. In
		practice this is used only with the classic tools' pane, and all classic
		tools provide a menu instead of a widget."""
		pass

	def update_for_new_tool(self, tool):
		"""Update the pane when a tool using it has just been activated. Widgets
		may be hidden/shown or enabled/disabled depending on the properties of
		the given tool."""
		pass

	def get_minimap_btn(self):
		pass

	def set_minimap_label(self, label):
		pass

	def hide_options_menu(self):
		pass

	def toggle_options_menu(self):
		pass

	def middle_click_action(self):
		pass

	def init_adaptability(self):
		"""Instructions to run during the first window size allocation (and only
		the first). Calling this is managed by the window's `DrOptionsManager`.
		It estimates the minimal amount of pixels for the mobile version, and
		gives it to the `_set_limit_size` method.
		Any implementation HAS TO end with a call to `_set_limit_size`!"""
		self.set_compact(False)
		self.action_bar.show_all()
		# + implementation-specific instructions

	def _set_limit_size(self, temp_limit_size):
		self._limit_size = int(1.25 * temp_limit_size)
		self.set_compact(True)

	def adapt_to_window_size(self, allocated_width):
		"""Check whether or not the costly `set_compact` method should be
		called, depending on a given window width, and the pane's limit
		previously set."""
		can_expand = (allocated_width > self._limit_size)
		incoherent = (can_expand == self._is_narrow)
		if incoherent:
			self.set_compact(not self._is_narrow)

	def set_compact(self, state):
		"""The parameter is a boolean telling if the bottom pane should become
		compact or not."""
		self._is_narrow = state
		if self.help_btn is not None:
			self.help_btn.set_visible(not state)
		# + implementation-specific instructions

	############################################################################
################################################################################

