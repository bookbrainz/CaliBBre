# -*- coding: utf8 -*-

# Copyright (C) 2015, 2016  Stanisław Szcześniak

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)
# noinspection PyUnresolvedReferences
from calibre.gui2.actions import InterfaceAction
# noinspection PyUnresolvedReferences
from calibre_plugins.CaliBBre.main import CaliBBreDialog

class Interface(InterfaceAction):
    name = 'CaliBBre'
    action_spec = ('CaliBBre', None, 'Query BB database', 'Ctrl+Shift+F2')

    def genesis(self):
        icon = get_icons('images/icon2b.png')
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        base_plugin_object = self.interface_action_base_plugin
        do_user_config = base_plugin_object.do_user_config
        d = CaliBBreDialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()
