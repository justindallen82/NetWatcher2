#
# gtkui.py
#
# Copyright (C) 2009 Riccardo Poggi <rik.poggi@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource

class GtkUI(GtkPluginBase):

    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        self.on_show_prefs()
        component.get("Preferences").add_page("NetWatcher2", self.glade.get_widget("prefs_box"))

        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

    def disable(self):
        component.get("Preferences").remove_page("NetWatcher2")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    def on_apply_prefs(self):
        log.debug("applying prefs for NetWatcher2")
        config = {}
        config["check_rate"] = self.glade.get_widget("spin_check_rate").get_value_as_int()
        config["download_rate"] = self.glade.get_widget("spin_dl_rate").get_value_as_int()
        config["ip_addresses"] = [addr.strip() for addr in self.glade.get_widget("addresses_entry").get_text().split(',')]
        config["custom_log"] = self.glade.get_widget("logging_check_button").get_active()
        config["log_dir"] = self.glade.get_widget("custom_logging_path").get_filename()

        client.netwatcher2.set_config(config)

    def on_show_prefs(self):
        client.netwatcher2.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        self.glade.get_widget("spin_check_rate").set_value(config["check_rate"])
        self.glade.get_widget("spin_dl_rate").set_value(config["download_rate"])
        self.glade.get_widget("addresses_entry").set_text(', '.join(config["ip_addresses"]))
        self.glade.get_widget("logging_check_button").set_active(config["custom_log"])
        self.glade.get_widget("custom_logging_path").set_filename(config["log_dir"])