# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

"""Defines ASGI runtime environment, log server, as well as background system tasks.
See :doc:`/plugins/linod`.

"""

import re
import datetime
from lino.api import ad, _

try:
    import channels
except ImportError:
    channels = None


class Plugin(ad.Plugin):
    """linod plugin"""
    verbose_name = _("Lino daemon")
    use_channels = False

    def on_plugins_loaded(self, site):
        assert self.site is site
        if self.use_channels:
            sd = site.django_settings
            # the dict that will be used to create settings
            cld = {}
            sd['CHANNEL_LAYERS'] = {"default": cld}
            sd['ASGI_APPLICATION'] = "lino.modlib.linod.routing.application"
            cld["BACKEND"] = "channels_redis.core.RedisChannelLayer"
            cld['CONFIG'] = {
                "hosts": [("localhost", 6379)],
                "channel_capacity": {
                    "http.request": 200,
                    "http.response!*": 10,
                    re.compile(r"^websocket.send\!.+"): 80,
                }
            }

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('linod.BackgroundTasks')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.system
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('linod.Procedures')

    def get_required_plugins(self):
        # we don't use needs_plugins because it depends on use_channels
        if self.use_channels:
            yield 'channels'

    def get_requirements(self, site):
        if self.use_channels:
            yield 'channels'
            yield 'channels_redis'
            yield 'daphne'

    def get_used_libs(self, html=None):
        if self.use_channels:
            if channels is None:
                version = self.site.not_found_msg
            else:
                version = channels.__version__
            yield ("Channels", version, "https://github.com/django/channels")
