# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
from typing import Callable
from django.conf import settings
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from lino.api import dd, _
from lino.core.roles import SiteStaff


class Procedure(dd.Choice):
    func: Callable
    # every_unit: str
    # every_value: int
    kwargs: dict

    def __init__(self, func, **kwargs):
        name = func.__name__
        super().__init__(name, name, name)
        self.func = func
        self.kwargs = kwargs
        # self.every_unit = every_unit
        # self.every_value = every_value

    async def run(self, ar):
        # raise Exception("20231014 Procedure.run()", self)
        # await database_sync_to_async(self.func)(ar)
        await sync_to_async(self.func)(ar)

    def __repr__(self):
        return f"Procedures.{self.value}"


class Procedures(dd.ChoiceList):
    verbose_name = _("Background procedure")
    verbose_name_plural = _("Background procedures")
    max_length = 100
    item_class = Procedure
    column_names = "value name text kwargs"
    # column_names = "value name text every_unit every_value"
    required_roles = dd.login_required(SiteStaff)

    @dd.virtualfield(dd.CharField(_("Suggested recurrency")))
    def kwargs(cls, choice, ar):
        return ", ".join(["{}={}".format(*i) for i in sorted(choice.kwargs.items())])

    # @dd.virtualfield(dd.CharField(_("Recurrency")))
    # def every_unit(cls, choice, ar):
    #     return choice.every_unit
    #
    # @dd.virtualfield(dd.CharField(_("Repeat every")))
    # def every_value(cls, choice, ar):
    #     return choice.every_value


class LogLevel(dd.Choice):
    num_value = logging.NOTSET
    def __init__(self, name):
        self.num_value = getattr(logging, name)
        super().__init__(name, name, name)

class LogLevels(dd.ChoiceList):
    verbose_name = _("Logging level")
    verbose_name_plural = _("Logging levels")
    item_class = LogLevel
    column_names = "value text num_value"

    @dd.virtualfield(dd.IntegerField(_("Numeric value")))
    def num_value(cls, choice, ar):
        return choice.num_value

LogLevel.set_widget_options('num_value', hide_sum=True)

add = LogLevels.add_item
add('DEBUG')
add('INFO')
add('WARNING')
add('ERROR')
add('CRITICAL')

# add('DEBUG', _("Include detailed debug messages"))
# add('INFO', _("Show informative messages"))
# add('WARNING', _("Only warnings and error messages"))
# add('ERROR', _("Only errors and critical messages"))
# add('CRITICAL', _("Only critical errors"))

# VERBOSITY_CHOICES = [
#    (0, _("silent")),
#    (1, _("normal")),
#    (2, _("verbose")),
#    (3, _("very verbose"))
# ]
